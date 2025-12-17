from pathlib import Path
import shutil
import sys
import os

import mutagen
import time

class SongOrganizer():
  def __init__(self, config, args):
    self.config = config
    self.args = args
  
  def _get_file_list(self,) -> list:
    return os.listdir(self.args.source_path)
  
  # artist, album, discnumber, tracknumber, title
  # there's also "date" and "albumartist"
  # TODO: make it customizable throught a .yaml file
  # TODO: make disc and tracknumber ignored through a flag
  # TODO: (?) make album ignored through a flag
  def _get_location(self, file_data, extension) -> tuple:
    path = os.path.join(self.args.path)
    if not file_data['artist']:
      return None
    if not file_data['title']:
      return None
    
    path = os.path.join(path, str(file_data['artist'][0]))

    if file_data["album"]:
      path = os.path.join(path, str(file_data['album'][0]))
    
    file_name = ""
    if 'discnumber' and 'tracknumber' in file_data:
      if file_data['discnumber'] and file_data['tracknumber']:
        nums = "%02d-%02d" % (int(file_data['discnumber'][0]), int(file_data['tracknumber'][0]), )
        file_name = f"{nums} {file_data['title'][0]}{extension}"
    elif 'tracknumber' in file_data:
      if file_data['tracknumber']:
        file_name = f"{file_data['tracknumber'][0]} {file_data['title'][0]}{extension}"
    else:
      file_name = f"{file_data['title'][0]}{extension}"

    return path, file_name

  def _place_file(self, file, location, name):
    if self.args.dry_run:
      return True
    
    if not os.path.exists(location):
      return False
    
    final_path = os.path.join(location, name)
    shutil.move(file, final_path)
    
    return True

  def _organize(self,):
    count_success = 0
    count_fail = 0

    print(f"[lyria] running organize on \"{self.args.source_path}\"")

    files = self._get_file_list() # get files from self.args.source_path
    for file in files:

      file = os.path.join(self.args.source_path, file)

      file_path = Path(file)
      file_data = mutagen.File(file, easy=True) # self.get_file_data(file)

      print(f" ~ process ~ {file_path}", end='\r')

      if not file_data:
        print(f" ~ fail/invalid ~ {file_path}")
        count_fail += 1
        continue

      location, file_name = self._get_location(file_data, ''.join(file_path.suffixes))
      if not location:
        print(f" ~ fail ~ file {file_path} doesn't contian essential tags.")
        count_fail += 1
        continue

      os.makedirs(location, exist_ok=True)
        #print(f" ~ fail ~ failed to create a directory structure for {file_path}")
        #count_fail += 1
        #continue

      success = self._place_file(file, location, file_name)
      if success:
        count_success += 1
      else:
        count_fail += 1
      pass

      sys.stdout.write("\r\033[K")
      print(f" ~ success ~ {file_path} => {location}/{file_name}")

    print(f"[lyria] done :3 \n moved - {count_success}\n failed - {count_fail}")

  def run(self,) -> int:
    if not self.args.path:
      print("[error] did not specify target path.")
      return -1
    if not self.args.source_path:
      print("[error] did not specify source path.")
      return -1
    
    if not os.path.exists(self.args.path):
      print("[error] invalid target path.")
      return 1
    if not os.path.exists(self.args.source_path):
      print("[error] invalid source path.")
      return 1
    
    self._organize()