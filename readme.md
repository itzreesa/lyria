# lyria
A tool for managing your songs!

## Installation (Automatic)
For `Linux` and `macOS`, use this command in terminal:

> `curl https://reesa.cc/lyria | sh`  

Make sure you have `python` installed, and `~/.local/bin` in your `$PATH`

## Installation (Manual)
- Install python3 (tested on 3.14)
- Clone or Download this repository somewhere safe.
- Create `~/.local/bin` and add it to your `PATH`
- Link `lyria.py` to `~/.local/bin/lyria`

## Updating
Use this command to update automatically to the newest tag.

> `lyria update` 

If this doesn't work, repeat the steps from manual installation section.

## Usage
lyria is split into components,  
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
If used `[--forget-not-found]`, for every song with no lyrics found, there will be an empty .lrc file written

Fetches synced lyrics, and writes it to the same path as file, with .lrc extension  

### 'organize' component
**See the explain [file](explain/organize.txt) for more.**  

> Usage: `lyria organize [target] [source] [--dry-run]`  

Iterates through every music file in [source] and reorganizes it in [target].  
The structure will look something like that: `Artist/Album/Disc-Track Title.Extension`  
For example: `Ado/Kyougen/01-11 Usseewa.mp3`

### 'cover' component
**See the explain [file](explain/cover.txt) for more.**  

> Usage: `lyria cover [target] [cover] [-r|--recursive] [--dry-run] [-f|--force]`

Sets art cover from `[cover]` for every file in `[target]` folder.
If used `[-r|--recursive]`, also processes sub-directories.
Does not replace covers, unless `[-f|--force]` is specified.