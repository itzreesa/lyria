
<p style="font-size: 2.6rem;font-weight:600;" align="center">☆:｡✱*. lyria ｡*✱.:｡</p>
<p align="center">
your music organizer
</br>
</br>
<img alt="GitHub Release" src="https://img.shields.io/github/v/release/itzreesa/lyria?style=flat-square&color=faa">
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/itzreesa/lyria?style=flat-square&color=fdf">
<img alt="GitHub License" src="https://img.shields.io/github/license/itzreesa/lyria?style=flat-square&color=aaf">
</br>
<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/itzreesa/lyria?style=flat-square&labelColor=4B8BBE&color=FFE873">
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/t/itzreesa/lyria?style=flat-square&color=bfb">
<img alt="Static Badge" src="https://img.shields.io/badge/made%20with-%3A3-d26?style=flat-square">
</br>
</p>

### Quickstart
Use [**pipx**](https://pipx.pypa.io/stable/) to install lyria.  
```bash
pipx install lyria
```
**pipx** manages a virtual environment automatically, so you don't need to worry about conflicting packages and their versions.  

# 
### Usage
The most basic thing you can use, is fetching lyrics for every file in the current working directory (non-recursively).  
```bash
lyria
```

lyria is split into *components*, explanation for them can be viewed using
```bash
lyria explain <component>
```
or you can view the text files in **[the explain](./src/lyria/explain/)** directory.

Below you can find a few examples,   
but I strongly recommend checking out the docs, so you can use *lyria* for what you actually need it for.

#### lyric grabbing
Fetch lyrics for folder `Music/` recursively.  
And for every song that you **can't find lyrics for**, create an **empty `.lrc` file** to skip it on the next run.
```bash
lyria lyrics Music/ -r --forget-not-found
```

Fetch lyrics in the current folder, recursively, **create a blank `.lrc` file** for every song, the lyrics **cannot be found for**, and **delete** the empty `.lrc` files, **older than 168h** (1 week).
```bash
lyria lyrics -r -n --forget-time=168
```

#### music organization
Get all the songs from folder `Import/` and organize them into the folder `Music/`.  
Perform a **dry run**, do not actually move files.
```bash
lyria organize Import/ Music/ --dry-run
```

#
### Conifguration
The config file should be located in `.config/lyria/config.ini`, on *nix systems.  
On win\*ows, it should be in `C:\Users\<User>\AppData\Local\lyria\config.ini`

Check the explanation files (`lyria explain <component>`), for the options inside the config files

# 
### Issues
If you're having an issue, or you have a proposal for a feature, please use the [Issues](https://github.com/itzreesa/lyria/issues) tab.

# 
### License
`lyria`'s source code is licensed under the MIT license. [here](./LICENSE)
<br></br>
#
###### thanks for reading me! ~readme file