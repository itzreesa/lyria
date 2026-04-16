from pathlib import Path
import traceback
import sys

import mutagen

from lyria.components.common import LYRIA_VERSION_FRIENDLY, progress_print

class SongOrganizer():
  def __init__(self, args, config):
    self.args = args
    self.config = config

    self.source = Path(self.args.source)
    self.target = Path(self.args.target)

    self.count_moved = 0
    self.count_warn = 0

  def print_stats(self,):
    if not self.args.silent:
      count_total = self.count_moved + self.count_warn
      print("\n== stats")
      print(f" ~ moved: {self.count_moved}")
      print(f" ~ warn: {self.count_warn}")
      print(f" ~~ total: {count_total}")

  def compose_file_path(self, file_data, extension) -> Path:
    # three parts, gathering data, composing directory structure and the file name
    # first part
    artist = file_data.get("artist", None)
    if not artist: 
      return None # type: ignore
    if len(artist) > 1:
      artist = '; '.join(artist)
    else:
      artist = artist[0]

    
    title = file_data.get("title", None)
    if not title: 
      return None # type: ignore
    title = title[0]
    
    album = file_data.get("album", None)
    if album:
      album = album[0]
    
    album_artist = file_data.get("albumartist", None)
    if album_artist:
      album_artist = album_artist[0]

    is_single = False
    if not album:
      is_single = True
    elif album == title:
      is_single = True
    elif "single" in album.lower():
      is_single = True

    disc_number = file_data.get("discnumber", None)
    track_number = file_data.get("tracknumber", None)

    # second part
    new_path = Path(self.target)

    directory_template = self.config.organize_template_directory
    if not directory_template or directory_template.replace(" ", "") == "":
      directory_template = "$artist/$album"

    if self.args.prefer_album_artist and album_artist:
      directory_template = directory_template.replace("$artist", album_artist)
    else:
      directory_template = directory_template.replace("$artist", artist)

    if not is_single and album and not self.config.organize_dummy_album:
      directory_template = directory_template.replace("$album", album)
    elif not album and self.config.organize_dummy_album:
      directory_template = directory_template.replace("$album", self.config.organize_dummy_album)
    else:
      directory_template = directory_template.replace("$album", "")

    if disc_number:
      directory_template = directory_template.replace("$discnumber", str(disc_number[0]))
    else:
      directory_template = directory_template.replace("$discnumber", "")
      

    new_path = new_path.joinpath(directory_template)

    if not self.args.dry_run:
      new_path.mkdir(parents=True, exist_ok=True)

    # third part
    # TODO: make it customizable in a config file
    file_name_template = self.config.organize_template_file
    if not file_name_template or file_name_template.replace(" ", "") == "":
      file_name_template = "$disc$title$extension"

    nums = ""
    if disc_number and track_number and not is_single:
      if disc_number == '1/1' or track_number == '1/1': # weird bug?
        nums = '1/1 - '
      else:
        nums = "%02d-%02d " % (int(disc_number[0]), int(track_number[0]))

    file_name = file_name_template
    file_name = file_name.replace("$disc", nums)
    file_name = file_name.replace("$title", title)
    if artist:
      if self.config.organize_prefer_album_artist:
        file_name = file_name.replace("$albumartist", album_artist)
      else:
        file_name = file_name.replace("$artist", artist)
    if album:
      file_name = file_name.replace("$album", album)
    else:
      file_name = file_name.replace("$album", "")
    if album_artist:
      file_name = file_name.replace("$albumartist", album_artist)
    elif not album_artist and artist: 
      file_name = file_name.replace("$albumartist", artist)
    else:
      file_name = file_name.replace("$albumartist", "")
    file_name = file_name.replace("$extension", extension)

    new_path = new_path / file_name

    return new_path

  def organize(self,):
    files = [file for file in self.source.iterdir()]
    for file in files:
      file_data = mutagen.File(file, easy=True) # type: ignore
      if not file_data:
        progress_print(self.args, 2, file)
        continue
      
      try:
        new_path = self.compose_file_path(file_data, file.suffix)
      except Exception:
        print(traceback.format_exc())
      if not new_path:
        progress_print(self.args, 1, file)
        continue

      if not self.args.dry_run:
        try:
          file.move(new_path)
          self.count_moved += 1
        except Exception:
          print(traceback.format_exc())
          progress_print(self.args, 6, file)
          self.count_warn += 1

      else:
        self.count_moved += 1

      if not self.args.silent:
        print(f" ~ {file} => {new_path}")

  def run(self,):
    if not self.source.exists():
      if not self.args.silent:
        print(" ~ error ~ invalid source path")
      return 1
    if not self.target.exists():
      if not self.args.silent:
        print(" ~ error ~ invalid target path")
      return
        
    self.organize()

    self.print_stats()