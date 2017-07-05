# Denite Github Stars 
`denite-github-stars` provides capabilities to fetch your starred repositories from github and select one for browsing. 

It's inspired by [helm-github-stars](https://github.com/Sliim/helm-github-stars).

## Requirments 
- [Denite](https://github.com/Shougo/denite.nvim)
- [wcwidth](https://pypi.python.org/pypi/wcwidth)

## Installation
```
Plug bennyyip/denite-github-stars
```

## Usage 
To show your starred repositories:
```
:Denite github_stars
```

## Setup your username 
Put the following line in your vimrc, change `bennyyip` to your username.
```
let dgs#username='bennyyip'
```

## Cache
At the first execution of `denite-github-stars`, list of repositories is fetched from github and saved into a cache file. 
The default cache location is `$XDG_CACHE_HOME/.cache/hgs-cache`(`~/.cache/github-stars` if `$XDG_CACHE_HOME` does not exist) 

## TODO
- [ ] Refresh cache
- [ ] Update the cache file automatically
- [ ] Private repo
- [ ] Customize cache dir
- [ ] Customize repo name align width
