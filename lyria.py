#!/usr/bin/env python3
from pathlib import Path
import sys
import os

import requests
import mutagen
import argparse

parser = argparse.ArgumentParser(
  prog="Lyria",
  description="lyrics fetcher",
  epilog="reesa <meow@reesa.cc> (github.com/itzreesa/lyria)"
)

parser.add_argument("path",
                    nargs="?",
                    default=".", 
                    type=str)
parser.add_argument("-v", "--verbose",
                    action="store_true",
                    default=False,
                    required=False)

class LyriaConfig():
  headers = None
  api_url = "https://lrclib.net/api/get?artist_name=$artist&track_name=$title"
  verbose = False
  search_dir = "."

class Lyria():
  def __init__(self, args):
    self.config = LyriaConfig()
    self.args = args
    self.setup()

  def setup(self,):
    self.config.headers = requests.utils.default_headers()
    self.config.headers.update(
      {
        'User-Agent': "lyria v1.0k (https://github.com/itzreesa/lyria)"
      }
    )

    self.config.search_dir = str(self.args.path)
    self.config.verbose = self.args.verbose

  def log(self, s):
    if self.config.verbose:
      print(s)

  def fetch_lyrics(self, artist, title) -> dict:
    request_url = self.config.api_url.replace("$artist", artist)
    request_url = request_url.replace("$title", title)
    request_url = request_url.replace(" ", "+")
  
    response = requests.get(url=request_url, headers=self.config.headers)
    if response.status_code == 404:
      print(f"[error] 404 on {artist} - {title}")
      return {}
  
    return response.json()

  def write_lyrics(self, file_name, data) -> bool:
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

  def process_files(self,) -> bool:
    os.chdir(self.config.search_dir)
    files = os.listdir()

    count_downloaded = 0
    count_exist = 0
    count_warn = 0

    for file in files:
      file_name = Path(file)
    
      if os.path.isdir(file):
        self.log(f"[skip/dir] {file_name}/")
        count_warn += 1
        continue

      file_data = mutagen.File(file, easy=True)
      if not file_data:
        self.log(f"[skip/invalid] {file_name}")
        count_warn += 1
        continue

      artist = file_data["artist"][0]
      title = file_data["title"][0]
    
      if os.path.exists(f"{file_name.stem}.lrc"):
        print(f"[exist] {artist} - {title}")
        count_exist += 1
        continue
    
      lyrics = self.fetch_lyrics(artist, title)
      if not lyrics:
        self.log(f"[warn] failed to fetch lyrics for {artist} - {title}")
        count_warn += 1
        continue
    
      success = self.write_lyrics(file_name.stem, lyrics)
      if not success:
        self.log(f"[error] failed to write lyrics for {artist} - {title}")
        return
      
      print(f"[ok] {artist} - {title}")
      count_downloaded += 1

    print(f"[lyria] done :3 \n downloaded - {count_downloaded}\n exist - {count_exist}\n warns - {count_warn}")

def main():
  args = parser.parse_args()
  ly = Lyria(args)
  ly.process_files()

if __name__ == "__main__":
  main()