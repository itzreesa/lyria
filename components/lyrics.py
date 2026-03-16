from pathlib import Path
import traceback
import time
import sys

import mutagen
import requests

from components.common import LYRIA_VERSION_FRIENDLY

class LyricFetcher():
  def __init__(self, debug, silent):
    self.API = "https://lrclib.net/api/"

    self.possible_queries = [
      [None, "get?artist_name=$artist&track_name=$title"],
      [None, "search?artist_name=$artist&track_name=$title"],
      ["album", "search?album_name=$album&track_name=$title"],
      ["album", "get?album_name=$album&track_name=$title"],
      ["albumartist", "get?album_name=$albumartist&track_name=$title"],
    ]

    self.silent = silent

    suffix = ""
    if debug:
      suffix = "-dev"
    self.headers = requests.utils.default_headers()
    self.headers.update(
      {
        'User-Agent': f"lyria {LYRIA_VERSION_FRIENDLY}{suffix} (https://github.com/itzreesa/lyria)"
      }
    )

  def fetch_lyrics(self, artist, title, album="", albumartist="") -> dict:
    for query in self.possible_queries:
      if query[0] == "album" and album == "":
        continue
      elif query[0] == "albumartist" and albumartist == "":
        continue

      q = query[1]
      q = q.replace("$artist", artist)
      q = q.replace("$title", title)
      if album:
        q = q.replace("$album", album)
      if albumartist:
        q = q.replace("$albumartist", albumartist)

      q = q.replace(" ", "+")

      response = requests.get(url=self.API+q, headers=self.headers)
      if response.status_code == 200:
        return response.json()
    
    if not self.silent:
      print(f"[error] {response.status_code} on {artist} - {title}")
    return {}

class LyricComponent():
  def __init__(self, args):
    self.args = args

    self.count_downloaded = 0
    self.count_exist = 0
    self.count_warn = 0
    self.count_total = 0
    self.count_processed = 0

    self.fetcher = LyricFetcher(args.debug, args.silent)

  def progress_print(self, ret, file: Path):
    if self.args.silent:
      return
    sys.stdout.write("\r\033[K")

    if self.args.verbose:
      file = file.absolute()

    match ret:
      case 0:
        print(" ~ success ~", file)
      case 1:
        print(" ~ fail ~", file)

      case 2:
        if self.args.verbose:
          print(" ~ fail/invalid ~", file)
      case 3:
        print(" ~ fail/fetch ~", file)
      case 4:
        print(" ~ fail/fetch-blank ~", file)
      case 5:
        print(" ~ fail/empty ~", file)

      case 11:
        if self.args.verbose:
          print(" ~ skip/exists ~", file)
      case 12:
        print(" ~ skip/instrumental ~", file)
      case 13:
        print(" ~ skip/blank ~", file)
      

      case _:
        print(" ~ fail ~", file)

  def print_stats(self,):
    if not self.args.silent:
      self.count_total = self.count_downloaded + self.count_exist + self.count_warn
      print("\n== stats")
      print(f" ~ downloaded: {self.count_downloaded}")
      print(f" ~ exist: {self.count_exist}")
      print(f" ~ warn: {self.count_warn}")
      print(f" ~~ total: {self.count_total}")

  def write_lyrics(self, path, data) -> int:
    lyrics = ""

    # forget not found
    if not data: 
      with open(path, 'w') as f:
        f.write(lyrics)
      return 13
    
    if type(data) == list:
      data = data[0]

    # write a blank, like fnf
    if data.get("instrumental", False):
      with open(path, 'w') as f:
        f.write(lyrics)
      return 12
    
    lyrics = data.get("syncedLyrics", False)
    if not lyrics:
      lyrics = data.get("plainLyrics", False)
    if not lyrics:
      return 4
    
    with open(path, 'w') as f:
      f.write(lyrics)

    return 0

  def process_file(self, path: Path) -> int:
    file_data = mutagen.File(path, easy=True) # type: ignore
    if not file_data:
      self.count_warn += 1
      return 2
    
    lrc_file_path = path.with_suffix(".lrc")
    if lrc_file_path.exists():
      if not self.args.forget_time:
        self.count_exist += 1
        return 11
      lrc_file_stat = lrc_file_path.lstat()
      if lrc_file_stat.st_size == 0:
        c_hour = time.time() // 3600
        f_hour = lrc_file_stat.st_ctime // 3600
        hours_passed = c_hour - f_hour
        # such a greatly designed control flow, right?
        if hours_passed >= self.args.forget_time:
          lrc_file_path.unlink()
        else:
          self.count_exist += 1
          return 11
      else:
        self.count_exist += 1
        return 11
    
    if self.args.dry_run:
      self.count_downloaded += 1
      return 0
    
    album = file_data.tags.get('album', None)
    artist = file_data.tags.get('artist', None)
    albumartist = file_data.tags.get('albumartist', None)
    title = file_data.tags.get('title', None)

    if album:
      album = album[0]
    if albumartist:
      albumartist = albumartist[0]

    if title == None:
      self.count_warn += 1
      return 2
    
    lyrics = self.fetcher.fetch_lyrics(
      artist=artist[0], 
      title=title[0],
      album=album,
      albumartist=albumartist
      )

    if not lyrics:
      self.count_warn += 1
      if self.args.forget_not_found:
        self.write_lyrics(lrc_file_path, None)
      return 3
    
    ret = self.write_lyrics(lrc_file_path, lyrics)
    if ret != 0:
      self.count_warn += 1
      return ret

    self.count_downloaded += 1  
    
    return 0

  def process_directory(self, path: Path):
    #print([x for x in path.iterdir() if x.is_dir()])
    if self.args.recursive:
      files = [file for file in path.walk()]
    else:
      files = [file for file in path.iterdir()]

    if len(files) == 0:
      self.progress_print(5, path)
      return

    # if only this path, files is a list of PosixPaths
    # if recursive, files is a list of tuples

    def do_files(paths):
      for file in paths:
        if file.is_file():
          if file.suffix == '.lrc':
            continue
          ret = 1
          try:
            ret = self.process_file(file)
          except Exception:
            print(traceback.format_exc())
          self.progress_print(ret, file)

    if not self.args.recursive:
      do_files(files)
      self.print_stats()
      return
    
    for walked_dir in files:
      base_dir, _, file_list = walked_dir # type: ignore
      new_file_list = []
      for file in file_list:
        f = Path(base_dir) / file
        new_file_list.append(f)

      do_files(new_file_list)

    self.print_stats()

  def run(self,) -> int:
    work_path = Path(self.args.path)
    
    if not work_path.exists():
      if not self.args.silent:
        print(" ~ error ~ invalid path")
        return 1

    if work_path.is_file():
      ret = self.process_file(work_path)
      self.progress_print(ret, work_path)
    else:
      self.process_directory(work_path)

    return 0
