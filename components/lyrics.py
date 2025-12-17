from pathlib import Path
import os

import requests
import mutagen

class LyricFetcher():
  def __init__(self, config, args):
    self.config = config
    self.args = args
    self.api_url = "https://lrclib.net/api/get?artist_name=$artist&track_name=$title"
    self.headers = requests.utils.default_headers()
    self._setup()

  def _setup(self,):
    self.headers.update(
      {
        'User-Agent': "lyria v1.0k (https://github.com/itzreesa/lyria)"
      }
    )

  def log(self, s):
    if self.config.verbose:
      print(s)

  def _fetch_lyrics(self, artist, title) -> dict:
    request_url = self.api_url.replace("$artist", artist)
    request_url = request_url.replace("$title", title)
    request_url = request_url.replace(" ", "+")
  
    response = requests.get(url=request_url, headers=self.headers)
    if response.status_code != 200:
      print(f"[error] {response.status_code} on {artist} - {title}")
      return {}
  
    return response.json()

  def _write_lyrics(self, file_name, data) -> bool:
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

  def run(self,) -> int:
    os.chdir(self.args.path)
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
    
      if self.config.dry_run:
        print(f"[ok/dry] {artist} - {title}")
        count_downloaded += 1
        continue
        
      lyrics = self._fetch_lyrics(artist, title)
      if not lyrics:
        self.log(f"[warn] failed to fetch lyrics for {artist} - {title}")
        count_warn += 1
        continue
    
      success = self._write_lyrics(file_name.stem, lyrics)
      if not success:
        self.log(f"[warn] failed to write lyrics for {artist} - {title}")
        count_warn += 1
        continue
      
      print(f"[ok] {artist} - {title}")
      count_downloaded += 1

    print(f"[lyria] done :3 \n downloaded - {count_downloaded}\n exist - {count_exist}\n warns - {count_warn}")
    return 0