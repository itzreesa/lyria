
<h1 align="center">lyria</h1>
<p align="center">
<strong>your new song manager</strong>
</br>
</br>
<img alt="GitHub Release" src="https://img.shields.io/github/v/release/itzreesa/lyria?style=flat-square&color=faa">
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/itzreesa/lyria?style=flat-square&color=fdf">
<img alt="GitHub License" src="https://img.shields.io/github/license/itzreesa/lyria?style=flat-square&color=aaf">
</br>
<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/itzreesa/lyria?style=flat-square&labelColor=4B8BBE&color=FFE873">
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/t/itzreesa/lyria?style=flat-square&color=bfb">
<img alt="Static Badge" src="https://img.shields.io/badge/made%20with-%3A3-d26?style=flat-square">
</p>

#

### Quickstart
On *Linux* and *macOS*, type this into your terminal.
```bash
curl https://reesa.cc/lyria | sh
```
**lyria** will be installed into `~/.local/share/lyria` and linked to `~/.local/bin`.  
Make sure it's in your `PATH`. And you have python installed.

#### Install manually (and windows)
Prepare folders `~/.local/share/lyria` and `~/.local/bin`  

**[Download](https://github.com/itzreesa/lyria/tarball/main)** the tarball from main branch or get the latest **[release](https://github.com/itzreesa/lyria/releases/latest)**

Unpack the tarball to `~/.local/share/lyria`

Make sure it's executable (windows doesn't need it)
```bash
chmod +x lyria.py
```
Link the executable (idk if it'll work on windows):
```bash
ln -sf "$HOME/.local/share/lyria/lyria.py" "$HOME/.local/bin/lyria"
```
If you haven't already, add `~/.local/bin` to your `PATH`!
```bash
# for bash
echo "export PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc

# for zsh
echo "export PATH=$HOME/.local/bin:$PATH" >> ~/.zshrc
```

Now, run `lyria` once to set up the venv and you'll be good to go!  
If there's a new version available, run this to update:
```bash lyria
lyria update
```

#
### Usage
lyria is split into *components*, explanation for them can be viewed using
```bash
lyria -e <component>
```
or you can see the text files in **[this](./explain/)** directory.

**Below you can find a few examples,   
but I strongly recommend checking out the docs, so you can use *lyria* for what you actually need it for.**

#### lyric grabbing
Fetch lyrics for all files in the current directory.  
The minimal example.
```bash
lyria
```

Fetch lyrics for folder `Music/` recursively.  
And for every song that you can't find lyrics for, create an empty file to skip it on next use.
```bash
lyria lyrics Music/ -r --forget-not-found
```

#### music organization
Get all the songs from folder `Import/` and organize them into the folder `Music/`.  
Force artist name to be "Mozart`.  
Perform a dry run, do not actually move files.
```bash
lyria organize Music/ Import/ --artist="Mozart" --dry-run
```

# 
### Issues
If you're having an issue, or you have a proposal for a feature, please use the [Issues](https://github.com/itzreesa/lyria/issues) tab.

# 
### License
`lyria`'s source code is licensed under the MIT license. [here](./LICENSE)

<br></br>
# 
###### thanks for reading me! ~readme file