# Lyria
Tool for managing your songs!

## Installation
- Install python (tested on 3.14)
- Clone or Download this repository somewhere safe.
- Download all the dependencies using `python -m pip install -r ./requirements.txt`
- Create `~/.local/bin` and add it to your `PATH`
- Link `lyria.py` to `~/.local/bin/lyria`

## Usage
Lyria is split into components,  
use `lyria --help` to see built-in help  
to see help for each component, run `lyria [component] -e` or `--explain`.

If you just want to grab lyrics for every song in the current folder (non-recursive), just run `lyria`.

## Components

### 'lyrics' component
**See the explain [file](explain/lyrics.txt) for more.**  

'lyrics' component is using [lrclib.net](https://lrclib.net/docs)'s [api] to fetch lyrics.  
> Usage: `lyria lyrics [path] [-r|--recursive] [--dry-run]`  
> Alternative: `lyria` => `lyria lyrics .`  

Scans selected `[path]`, defaults to the current directory, for music files.
If used `[-r|--recursive]`, also scans sub-directories.

Fetches synced lyrics, and writes it to the same path as file, with .lrc extension  

### 'organize' component
**See the explain [file](explain/organize.txt) for more.**  

> Usage: `lyria organize [target] [source] [--dry-run]`  

Iterates through every music file in [source] and reorganizes it in [target].  
The structure will look something like that: `Artist/Album/Disc-Track Title.Extension`  
For example: `Ado/Kyougen/01-11 Usseewa.mp3`