from pathlib import Path
import sys
import os

import requests
import mutagen

from components.common import extract_tags

class LyricFetcher():
  def __init__(self, config, args):
    self.config = config
    self.args = args
    self.api_url = "https://lrclib.net/api/get?artist_name=$artist&track_name=$title"
    self.headers = requests.utils.default_headers()
    self.count_downloaded = 0
    self.count_exist = 0
    self.count_warn = 0

    self.count_total = 0
    self.count_processed = 0
    self._setup()

  def _setup(self,):
    self.headers.update(
      {
        'User-Agent': f"lyria {self.config._version_friendly} (https://github.com/itzreesa/lyria)"
      }
    )

  def _ret_print(self, ret, file):
    sys.stdout.write("\r\033[K")
    match ret:
      case 0:
        print(" ~ success ~ ", os.path.abspath(file))

      case 2:
        print(" ~ fail/invalid ~ ", os.path.abspath(file))
      case 3:
        print(" ~ fail/fetch ~ ", os.path.abspath(file))

      case 11:
        print(" ~ skip/exists ~ ", os.path.abspath(file))
      case 12:
        print(" ~ skip/instrumental ~ ", os.path.abspath(file))
      case 13:
        print(" ~ skip/blank ~ ", os.path.abspath(file))

      case _:
        print(" ~ fail ~ ", os.path.abspath(file))

  def _fetch_lyrics(self, artist, title) -> dict:
    request_url = self.api_url.replace("$artist", artist)
    request_url = request_url.replace("$title", title)
    request_url = request_url.replace(" ", "+")
  
    response = requests.get(url=request_url, headers=self.headers)
    if response.status_code != 200:
      print(f"[error] {response.status_code} on {artist} - {title}")
      return {}
  
    return response.json()

  def _write_lyrics(self, file_name, data) -> int:
    lyrics = ""
    if not data:
      with open(f"{file_name}.lrc", 'w') as f:
        f.write(lyrics)
      return 13
    if data["instrumental"]:
      # write blank file so we don't call the api too many times
      with open(f"{file_name}.lrc", 'w') as f:
        f.write(lyrics)
      return 12

    if data["syncedLyrics"]:
      lyrics = data["syncedLyrics"]
    elif data["plainLyrics"]:
      lyrics = data["plainLyrics"]
    else:
      print(f"(?) No lyrics found for {file_name}")
      if self.config.verbose:
        print(f"\tdata => {data}")
      return 1
  
    with open(f"{file_name}.lrc", 'w') as f:
      f.write(lyrics)

    return 0

  def _process_file(self, file) -> int:
    file_data = mutagen.File(file, easy=True)
    if not file_data:
      self.count_warn += 1
      return 2
    
    artist, _, title = extract_tags(file_data, self.args)

    file_name = Path(file)
    if os.path.exists(f"{file_name.stem}.lrc"):
      self.count_exist += 1
      return 11
    
    if self.config.dry_run:
      self.count_downloaded += 1
      return 0
      
    lyrics = self._fetch_lyrics(artist, title)
    if not lyrics:
      self.count_warn += 1
      if self.args.forget_not_found:
        self._write_lyrics(file_name.stem, None)
      return 3

    ret = self._write_lyrics(file_name.stem, lyrics)
    if ret != 0:
      self.count_warn += 1
      return ret

    self.count_downloaded += 1
    return 0

  def _process_directory(self, directory) -> tuple:
    os.chdir(directory)
    files = os.listdir()

    self.count_total += len(files)

    for file in files:
      file_name = Path(file)
      self.count_processed = self.count_downloaded + self.count_exist + self.count_warn
      sys.stdout.write("\r\033[K")
      print(f" ~ {self.count_processed}/{self.count_total} ~ {os.path.abspath(file)}", end='\r')
      if file_name.stem.startswith('.'):
        if self.config.verbose:
          sys.stdout.write("\r\033[K")
          print(f" ~ skip/hidden ~ {os.path.abspath(file)}")
        self.count_warn += 1
        continue

      if ".lrc" in file_name.suffixes:
        self.count_total -= 1
        continue

      if os.path.isdir(file):
        if self.config.verbose:
          sys.stdout.write("\r\033[K")
        if self.config.recursive:
          if self.config.verbose:
            print(" ~ processing directory ~ ", os.path.abspath(file))
          self._process_directory(file)
          os.chdir("..")
          continue
        
        if self.config.verbose:
          print(" ~ skip/dir ~ ", os.path.abspath(file))
        continue
      
      ret = self._process_file(file,)
      if self.config.verbose:
        sys.stdout.write("\r\033[K")
        self._ret_print(ret, file)

  def run(self,) -> int:
    if os.path.isdir(self.args.path):
      self._process_directory(self.args.path)
    else:
      file = self.args.path
      path = os.path.dirname(os.path.realpath(file))
      os.chdir(path)
      file = os.path.basename(file)
      print(f" ~ single file => {file} ", end='\r')
      ret = self._process_file(file,)
      self._ret_print(ret, file)
        
    sys.stdout.write("\r\033[K")
    print(f"[lyria] done :3 \n downloaded - {self.count_downloaded}\n exist - {self.count_exist}\n warns - {self.count_warn}")
    return 0