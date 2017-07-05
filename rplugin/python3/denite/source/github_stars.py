from urllib.request import urlopen
import json
import os
from wcwidth import wcswidth
from .base import Base


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'github_stars'
        self.kind = 'file'
        self.username = self.vim.vars['dgs#username']
        cache_dir = os.path.join(
            os.path.expanduser(os.getenv('XDG_CACHE_HOME', '~/.cache')),
            'github_stars')
        self.cache_dir = os.path.normpath(cache_dir)
        self.cache_file = os.path.join(cache_dir, 'starred_repos')

    def gather_candidates(self, context):
        repos = self.get_repos()
        candidates = []
        for (name, url, desc) in repos:
            candidates.append({
                "word": name + desc,
                "action__path": url,
                "abbr": abbr(name, desc)
            })
        return candidates

    def get_repos(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        if not os.path.exists(self.cache_file):
            self.fetch_from_github()
        return self.read_cache()

    def read_cache(self):
        with open(self.cache_file, 'rb') as f:
            return [parse_line(line.decode('utf-8')) for line in f.readlines()]

    def fetch_from_github(self):
        print("fetching starred repos of %s" % self.username)
        with open(self.cache_file, 'wb') as f:
            page = 1
            while True:
                resp = fetch_page(self.username, page)
                page += 1
                starred_repos = json.load(resp)
                if len(starred_repos) == 0:
                    print(page)
                    break
                for repo in starred_repos:
                    f.write(("%s %s %s\n" %
                             (repo['full_name'], repo['html_url'], ""
                              if repo['description'] is None else
                              repo['description'])).encode('utf-8'))


def abbr(name, desc):
    name = name[:25]
    desc = desc[:50].strip()
    spaces = 30 - wcswidth(name)
    return name + spaces * ' ' + desc


def fetch_page(username, page):
    resp = urlopen(
        "https://api.github.com/users/%s/starred?per_page=100&page=%d" %
        (username, page))
    return resp


def parse_line(line):
    name, sep, rest = line.partition(" ")
    url, sep, desc = rest.partition(" ")
    return name, url, desc
