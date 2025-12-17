# Lyria
Tool for automatically grabbing lyrics for every song in folder  
Using [lrclib.net](https://lrclib.net)'s [api](https://lrclib.net/docs)

## Installation
- Clone or Download this repository somewhere safe.
- Download all the dependencies using `python -m pip install -r ./requirements.txt`
- Create `~/.local/bin` and add it to your `PATH`
- Link `lyria.py` to `~/.local/bin/lyria`

## Usage
- Navigate to folder containing your music
- Use `lyria` to automatically fetch lyrics for every song in the current folder (non-recursive)
- Use `lyria -v` to see verbose output (skipped, invalid, etc.)
- Use `lyria <path>` for example `lyria my_artist/` to use lyria on specified path