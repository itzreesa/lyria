from pathlib import Path
import sys
import os

from mutagen.id3 import APIC, PictureType
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3
from PIL import Image

# stolen from stackoverflow muhehehe
MODE_TO_BPP = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}

class CoverPainter():
  def __init__(self, config, args):
    self.config = config
    self.args = args
    self.count_painted = 0
    self.count_exist = 0
    self.count_warn = 0

    self.cover_data = None
    self.cover_width = None
    self.cover_height = None
    self.cover_depth = None

  def _ret_print(self, ret, file):
    sys.stdout.write("\r\033[K")
    match ret:
      case 0:
        print(f" ~ success => {self.args.path}")
      case 2:
        print(f" ~ fail/unsupported => {self.args.path}")
      case 11:
        print(f" ~ skip/exists => {self.args.path}")
      case _:
        print(f" ~ fail => {self.args.path}")

  def _convert_cover_file(self,) -> bool:
    img = None
    try:
      img = Image.open(self.args.source_path)
    except Exception as e:
      print(f"[error] can't open file: {e}")
    try:
      img = img.convert("RGB")
      img.save(".lyria_cover.tmp", "JPEG")
    except Exception as e:
      print(f"[error] can't convert file: {e}")
    self.cover_data = open(self.args.source_path, 'rb').read()
    self.cover_width, self.cover_height = img.size
    self.cover_depth = MODE_TO_BPP[img.mode]

  def _paint_id3(self, file):
    audio = MP3(file)
    if audio.tags.getall("APIC") and not self.config.force:
      return 11
    audio.tags.delall("APIC")
    audio.tags.add(
      APIC(3, 'image/jpeg', 3, "Cover", self.cover_data)
    )
    if not self.config.dry_run:
      audio.save(file)
    return 0

  def _paint_flac(self, file):
    audio = FLAC(file)
    if audio.pictures and not self.config.force:
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
    if not self.config.dry_run:
      audio.save()
    return 0

  def _paint_mp4(self, file):
    audio = MP4(file)
    if "covr" in audio.tags and not self.config.force:
      return 11
    cover = MP4Cover(self.cover_data, MP4Cover.FORMAT_JPEG)
    audio["covr"] = [cover]
    if not self.config.dry_run:
      audio.save()
    return 0

  def _process_file(self, file):
    file_name = Path(file)
    suffix = file_name.suffix
    if ".mp3" in suffix:
      return self._paint_id3(file)
    elif ".flac" in suffix:
      return self._paint_flac(file)
    elif ".m4a" in suffix:
      return self._paint_mp4(file)
    else:
      return 2

  def _process_directory(self, directory):
    os.chdir(directory)
    files = os.listdir()

    for file in files:
      file_name = Path(file)
      print(f" ~ process ~ {os.path.abspath(file)}", end='\r')
      if file_name.stem.startswith('.'):
        sys.stdout.write("\r\033[K")
        print(f" ~ skip/hidden ~ {os.path.abspath(file)}")
        self.count_warn += 1
        continue

      if os.path.isdir(file):
        sys.stdout.write("\r\033[K")
        if self.config.recursive:
          print(" ~ processing directory ~ ", os.path.abspath(file))
          self._process_directory(file)
          os.chdir("..")
          continue
  
        print(" ~ skip/dir ~ ", os.path.abspath(file))
        continue
      
      ret = self._process_file(file,)
      sys.stdout.write("\r\033[K")
      self._ret_print(ret, file)

  def run(self,):
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

    self._convert_cover_file()
    print(f"[cover] using cover file: {self.args.source_path} => .lyria_cover.tmp (JPEG)")

    if os.path.isdir(self.args.path):
      self._process_directory(self.args.path)
    else:
      file = self.args.path
      print(f" ~ single file => {file} ", end='\r')
      ret = self._process_file(file)
      self._ret_print(ret, file)
      
    print(f"[cover] deleting temp file .lyria_cover.tmp")
    if os.path.exists(".lyria_cover.tmp"):
      os.remove(".lyria_cover.tmp")
  
    print(f"[lyria] done :3 \n painted - {self.count_painted}\n exist - {self.count_exist}\n warns - {self.count_warn}")
    return 0