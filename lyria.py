#!/usr/bin/env python3
from pathlib import Path

import os

import requests
import mutagen

global HEADERS
SEARCH_PATH = "."
HEADERS = None
API_URL = "https://lrclib.net/api/get?artist_name=$artist&track_name=$title"
#ALLOWED_EXTENSIONS = ['.mp3', '.mp4', '.flac', '.ogg',' .m4a', '.opus', '.wav', '.aac']

VERBOSE = False

def log(s):
  if VERBOSE:
    print(s)

def get_lyrics(artist, title) -> dict:
  request_url = API_URL.replace("$artist", artist)
  request_url = request_url.replace("$title", title)
  request_url = request_url.replace(" ", "+")
  
  response = requests.get(url=request_url, headers=HEADERS)
  if response.status_code == 404:
    print(f"Error 404 on {artist} - {title}")
    return {}
  
  return response.json()

def write_lyrics(file_name, data) -> bool:
  lyrics = ""
  if data["syncedLyrics"]:
    lyrics = data["syncedLyrics"]
  elif data["plainLyrics"]:
    lyrics = data["plainLyrics"]
  else:
    print(f"(?) No lyrics found for {file_name}")
    return False
  
  with open(f"{file_name}.lrc", 'w') as f:
    f.write(lyrics)

  return True

def process(folder):
  #pawd = os.getcwd()
  songs = os.listdir()
  for song in songs:
    file_name = Path(song)
    
    if os.path.isdir(song):
      log(f"[skip/dir] {file_name}/")
      continue

    file_data = mutagen.File(song, easy=True)
    if not file_data:
      log(f"[skip/invalid] {file_name}")
      continue

    artist = file_data["artist"][0]
    title = file_data["title"][0]
    
    if os.path.exists(f"{file_name.stem}.lrc"):
      log(f"[exist] {artist} - {title}")
      continue
    
    lyrics = get_lyrics(artist, title)
    if not lyrics:
      return
    
    success = write_lyrics(file_name.stem, lyrics)
    if not success:
      return
    print(f"[ok] {artist} - {title}")

def setup():
  global HEADERS
  HEADERS = requests.utils.default_headers()
  HEADERS.update(
    {
      'User-Agent': "lyria v0.1 (WIP) (https://github.com/itzreesa)"
    }
  )

def main():
  setup()
  process(SEARCH_PATH)
  print("[lyria] all okay :3")

if __name__ == "__main__":
  main()
