from platformdirs import PlatformDirs
from pathlib import Path

import configparser
import tomllib

dirs = PlatformDirs("lyria")

class LyriaConfig:
  def __init__(self,):
    self.config_dir = Path(dirs.user_config_dir)
    self.config_file = self.config_dir / "config.toml"

    self.config = configparser.ConfigParser()

    self.lyrics_forget_not_found = False
    self.lyrics_forget_time = 0
    
    self.organize_prefer_album_artist = True
    self.organize_template_directory = "$artist/$album/"
    self.organize_template_file = "$disc$title$extension"
    self.organize_dummy_album = ""

  def save_config(self,):
    if not self.config.has_section("lyrics"):
      self.config.add_section("lyrics")
    if not self.config.has_section("organize"):
      self.config.add_section("organize")
    self.config["lyrics"] = { # type: ignore
      "forget_not_found": self.lyrics_forget_not_found,
      "forget_time": self.lyrics_forget_time
    }

    self.config["organize"] = { # type: ignore
      "prefer_album_artist": self.organize_prefer_album_artist,
      "template_directory": self.organize_template_directory,
      "template_file": self.organize_template_file,
      "dummy_album": self.organize_dummy_album
    }
    self.config_dir.mkdir(parents=True,exist_ok=True)
    with open(self.config_file, 'w') as f:
      self.config.write(f)

  def load_config(self,):
    if not self.config_file.exists():
      self.save_config()
      return
    with open(self.config_file, 'r') as f:
      self.config.read_file(f)
    
    self.lyrics_forget_not_found = self.config["lyrics"].getboolean("forget_not_found", False)
    self.lyrics_forget_time = self.config["lyrics"].getint("forget_time", 0)
    self.organize_prefer_album_artist = self.config["organize"].getboolean("prefer_album_artist", True)
    self.organize_template_directory = self.config["organize"].get("template_directory", "$artist/$album/")
    self.organize_template_file = self.config["organize"].get("template_file", "$disc$title$extension")
    self.organize_dummy_album = self.config["organize"].get("dummy_album", "")