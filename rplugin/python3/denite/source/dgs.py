from urllib.request import urlopen
import json
import os
import vim
from wcwidth import wcswidth
from .base import Base

username = vim.vars['dgs#username'].decode()
cache_file = os.path.join(
    os.path.expanduser(os.getenv('XDG_CACHE_HOME', '~/.cache')), 'dgs',
    'starred_repos')


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'gs'
        self.kind = 'file'

    def gather_candidates(self, context):
        repos = get_repos()
        candidates = []
        for (name, url, desc) in repos:
            candidates.append({
                "word": name + desc,
                "action__path": url,
                "abbr": abbr(name, desc)
            })
        return candidates


def get_repos():
    if not os.path.exists(cache_file):
        fetch(username)
    return read_cache()


def abbr(name, desc):
    name = name[:25]
    desc = desc[:50]
    spaces = 30 - wcswidth(name)
    return name + spaces * ' ' + desc


def fetch(username):
    print("fetching starred repos of %s" % username)
    with open(cache_file, 'w') as f:
        page = 1
        while True:
            resp = fetch_page(username, page)
            page += 1
            starred_repos = json.load(resp)
            if len(starred_repos) == 0:
                print(page)
                break
            for repo in starred_repos:
                f.write(
                    "%s %s %s\n" %
                    (repo['full_name'], repo['html_url'], ""
                     if repo['description'] is None else repo['description']))


def fetch_page(username, page):
    resp = urlopen(
        "https://api.github.com/users/%s/starred?per_page=100&page=%d" %
        (username, page))
    return resp


def read_cache():
    with open(cache_file, 'r') as f:
        return [parse_line(line) for line in f.readlines()]


def parse_line(line):
    name, sep, rest = line.partition(" ")
    url, sep, desc = rest.partition(" ")
    return name, url, desc
