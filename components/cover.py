from pathlib import Path
import traceback
import sys

from mutagen.id3 import APIC, PictureType # type: ignore
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3
from PIL import Image

from components.common import progress_print

# stolen from stackoverflow muhehehe
MODE_TO_BPP = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}

class CoverPainter():
  def __init__(self, args):
    self.args = args
    self.count_painted = 0
    self.count_exist = 0
    self.count_warn = 0

    self.cover_data = None
    self.cover_width = None
    self.cover_height = None
    self.cover_depth = None

    self.source = None

  def print_stats(self,):
    if not self.args.silent:
      self.count_total = self.count_painted + self.count_exist + self.count_warn
      print("\n== stats")
      print(f" ~ downloaded: {self.count_painted}")
      print(f" ~ exist: {self.count_exist}")
      print(f" ~ warn: {self.count_warn}")
      print(f" ~~ total: {self.count_total}")

  def _convert_cover_file(self,) -> int:
    img = None
    try:
      img = Image.open(self.source) # type: ignore
    except Exception as e:
      print(f"[error] can't open file: {e}")
      print(traceback.format_exc())
      return 1
    try:
      img = img.convert("RGB")
      img.save(".lyria_cover.tmp", "JPEG")
    except Exception as e:
      print(f"[error] can't convert file: {e}")
    self.cover_data = open(self.source, 'rb').read() # type: ignore
    self.cover_width, self.cover_height = img.size
    self.cover_depth = MODE_TO_BPP[img.mode]
    return 0

  def _paint_id3(self, file):
    audio = MP3(file)
    if audio.tags.getall("APIC") and not self.args.force: # type: ignore
      return 11
    audio.tags.delall("APIC") # type: ignore
    audio.tags.add( # type: ignore
      APIC(3, 'image/jpeg', 3, "Cover", self.cover_data)
    )
    if not self.args.dry_run:
      audio.save(file)
    return 0

  def _paint_flac(self, file):
    audio = FLAC(file)
    if audio.pictures and not self.args.force:
      return 11
    else:
      audio.clear_pictures()
    picture = Picture()
    picture.data = self.cover_data
    picture.type = PictureType.COVER_FRONT
    picture.mime = u"image/jpeg"
    picture.width = self.cover_width
    picture.height = self.cover_height
    picture.depth = self.cover_depth
    audio.add_picture(picture)
    if not self.args.dry_run:
      audio.save()
    return 0

  def _paint_mp4(self, file):
    audio = MP4(file)
    if "covr" in audio.tags and not self.args.force: # type: ignore
      return 11
    cover = MP4Cover(self.cover_data, MP4Cover.FORMAT_JPEG)
    audio["covr"] = [cover]
    if not self.args.dry_run:
      audio.save()
    return 0

  def process_file(self, file):
    suffix = file.suffix
    if ".mp3" in suffix:
      return self._paint_id3(file)
    elif ".flac" in suffix:
      return self._paint_flac(file)
    elif ".m4a" in suffix:
      return self._paint_mp4(file)
    else:
      return 7

  def process_directory(self, path):
    if self.args.recursive:
      files = [file for file in path.walk()]
    else:
      files = [file for file in path.iterdir()]

    if len(files) == 0:
      progress_print(self.args, 5, path)
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
          progress_print(self.args, ret, file)

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

  def run(self,):
    target = Path(self.args.target)
    self.source = Path(self.args.source)

    if not target.exists():
      if not self.args.silent:
        print(" ~ error ~ invalid target path.")
      return 1
    
    if not self.source.exists():
      if not self.args.silent:
        print(" ~ error ~ invalid source path.")
      return 1

    ret = self._convert_cover_file()
    if ret == 1:
      if not self.args.silent:
        print(" ~ error ~ cannot convert cover file")
      return ret
    if not self.args.silent:
      print(f" ~ using cover file: {self.source} => .lyria_cover.tmp (JPEG)")
    
    if target.is_file():
      ret = self.process_file(target)
      progress_print(self.args, ret, target)
    else:
      self.process_directory(target)

    cover_path = Path(".lyria_cover.tmp")
    if cover_path.exists():
      cover_path.unlink()
    
    return 0
