from .base import Base
from urllib.request import urlopen
import json
import os

username = "bennyyip"
cache_file = os.path.join(
    os.path.expanduser(os.getenv('XDG_CACHE_HOME', '~/.cache')), 'dgs',
    'starred_repos')


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'gs'
        self.kind = 'file'

    def gather_candidates(self, context):
        repos = read_cache()
        candidates = []
        for (name, url, desc) in repos:
            candidates.append({"word": name, "action__path": url})
        return candidates


def fetch():
    resp = urlopen("https://api.github.com/users/%s/starred" % username)
    starred_repos = json.load(resp)
    with open(cache_file, 'w') as f:
        for repo in starred_repos:
            f.write("%s %s %s\n" %
                    (repo['full_name'], repo['html_url'], ""
                     if repo['description'] is None else repo['description']))


def read_cache():
    with open(cache_file, 'r') as f:
        return [parse_line(line) for line in f.readlines()]


def parse_line(line):
    name, sep, rest = line.partition(" ")
    url, sep, desc = rest.partition(" ")
    return name, url, desc
