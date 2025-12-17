#!/usr/bin/env python3

from components.lyrics import LyricFetcher
from components.organize import SongOrganizer
from components.cover import CoverPainter

from explain import LyriaExplain

import argparse

LYRIA_VERSION_MAJOR = 1
LYRIA_VERSION_MINOR = 2
LYRIA_VERSION_PATCH = 1

LYRIA_VERSION_FRIENDLY = f"{LYRIA_VERSION_MAJOR}.{LYRIA_VERSION_MINOR}.{LYRIA_VERSION_PATCH}"

parser = argparse.ArgumentParser(
  prog="lyria",
  description="your silly song manager",
  epilog=f"lyria {LYRIA_VERSION_FRIENDLY} by reesa <meow@reesa.cc> (github.com/itzreesa/lyria)"
)

# components
parser.add_argument("component",
                    help="select component used",
                    choices=["lyrics", "organize", "cover"],
                    default="lyrics",
                    const="lyrics",
                    nargs="?",
                    type=str)

# positionals
parser.add_argument("path",
                    help="base path, used as target for components",
                    default=".", 
                    nargs="?",
                    type=str)
parser.add_argument("source_path", # used for organizer
                    help="source path, used as input for certain components",
                    default=None, 
                    nargs="?",
                    type=str)

# toggles
parser.add_argument("-r", "--recursive",
                    help="toggle recursive mode, doesn't work for organizer mode",
                    action="store_true",
                    default=False,
                    required=False)
parser.add_argument("-f", "--force",
                    help="force operation on files",
                    action="store_true",
                    default=False,
                    required=False)
parser.add_argument("--dry-run",
                    help="toggle dry run, process files without doing anything",
                    action="store_true",
                    default=False,
                    required=False)
parser.add_argument("-e", "--explain",
                    help="toggle explain selected component",
                    action="store_true",
                    default=False,
                    required=False)

# about
parser.add_argument("-v", "--verbose",
                    help="toggle more verbose output, e.g. skipped, invalid entries",
                    action="store_true",
                    default=False,
                    required=False)
parser.add_argument("--debug",
                    help="toggle debug mode",
                    action="store_true",
                    default=False,
                    required=False)

class LyriaConfig():
  dry_run = False
  verbose = False
  debug = False
  _version_friendly = LYRIA_VERSION_FRIENDLY

class Lyria():
  def __init__(self, args):
    self.config = LyriaConfig()
    self.args = args
    self._setup()
    
  def _setup(self,):
    self.config.recursive = self.args.recursive
    self.config.force = self.args.force
    self.config.dry_run = self.args.dry_run
    self.config.verbose = self.args.verbose
    self.config.debug = self.args.debug

  def start(self,):
    if self.config.debug:
      print(f"[debug] argparse: {self.args}")

    component = None

    if self.args.explain:
      component = LyriaExplain(self.args.component)
      component.run()
      exit(0)

    ret = 0

    match self.args.component:
      case "lyrics":
        component = LyricFetcher(self.config, self.args)
      case "organize":
        component = SongOrganizer(self.config, self.args)
      case "cover":
        component = CoverPainter(self.config, self.args)
      case _:
        parser.print_help()
        exit(1)
        
    ret = component.run()

    if ret == -1:
      parser.print_usage()
      
def main():
  args = parser.parse_args()
  ly = Lyria(args)
  ly.start()

if __name__ == "__main__":
  main()