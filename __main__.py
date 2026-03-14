#!/usr/bin/env python3

from components.lyrics import LyricComponent
from components.organize import SongOrganizer
from components.cover import CoverPainter

from explain import LyriaExplain

import argparse

from components.common import LYRIA_VERSION_FRIENDLY

epilog=f"lyria {LYRIA_VERSION_FRIENDLY} by reesa <meow@reesa.cc> (https://github.com/itzreesa/lyria)"


parser = argparse.ArgumentParser(
  prog="lyria",
  description="your silly song manager",
  epilog=epilog
)

parser.add_argument("-v", "--verbose",
                    help="toggle more verbose output, e.g. skipped, invalid entries",
                    action="store_true",
                    default=False,
                    required=False)
parser.add_argument("-s", "--silent",
                    help="disables all printed output, for scripting",
                    action="store_true",
                    default=False,
                    required=False)
parser.add_argument("-V", "--version",
                    help="print the version and quit",
                    action="store_true",
                    default=False,
                    required=False)
parser.add_argument("--debug",
                    help="toggle debug mode",
                    action="store_true",
                    default=False,
                    required=False)

subparsers = parser.add_subparsers(
  title="components",
  description="components avaliable to select",
  dest="component",
  required=False
)

parser.set_defaults(component="lyrics", path=".", recursive=False, dry_run=False, forget_not_found=False)

# lyrics
parser_lyrics = subparsers.add_parser("lyrics", epilog=epilog)
parser_lyrics.add_argument("path",
                    help="work path, where the component will work in, defaults to the current directory or a single file",
                    default=".",
                    nargs="?",
                    type=str)
parser_lyrics.add_argument("-r", "--recursive",
                    help="scans children of the work directory, and recursively..",
                    action="store_true",
                    default=False,
                    required=False)
parser_lyrics.add_argument("-d", "--dry-run",
                    help="parse files, without fetching lyrics",
                    action="store_true",
                    default=False,
                    required=False)
parser_lyrics.add_argument("-n", "--forget-not-found",
                    help="if cannot find lyrics, creates an empty placeholder file",
                    action="store_true",
                    default=False,
                    required=False)
parser_lyrics.add_argument("--forget-time",
                    help="age (in days) of empty .lrc files that will be respected upon this fetch",
                    required=False,
                    nargs="?",
                    type=int)

# organize
praser_organize = subparsers.add_parser("organize", epilog=epilog)
praser_organize.add_argument("source",
                    help="path, from where the files will be taken",
                    default=".",
                    nargs="?",
                    type=str)
praser_organize.add_argument("target",
                    help="directory, where the files will be organized in",
                    default=None,
                    nargs="?",
                    type=str)
praser_organize.add_argument("-d", "--dry-run",
                    help="parse files, without fetching lyrics",
                    action="store_true",
                    default=False,
                    required=False)
praser_organize.add_argument("--artist",
                    help="override artist name",
                    nargs="?",
                    default=None,
                    required=False)
praser_organize.add_argument("--album",
                    help="override album name",
                    nargs="?",
                    default=None,
                    required=False)
praser_organize.add_argument("--album-artist",
                    help="override album artist name",
                    nargs="?",
                    default=None,
                    required=False)

# cover
parser_cover = subparsers.add_parser("cover", epilog=epilog)
parser_cover.add_argument("source",
                    help="path to the cover image",
                    default=".",
                    nargs="?",
                    type=str)
parser_cover.add_argument("target",
                    help="file or directory of files to apply covers there",
                    default=None,
                    nargs="?",
                    type=str)
parser_cover.add_argument("-f", "--force",
                    help="force overwrite image data if it exists already",
                    action="store_true",
                    default=False,
                    required=False)
parser_cover.add_argument("-r", "--recursive",
                    help="scans children of the work directory, and recursively..",
                    action="store_true",
                    default=False,
                    required=False)
parser_cover.add_argument("-d", "--dry-run",
                    help="parse files, without fetching lyrics",
                    action="store_true",
                    default=False,
                    required=False)

# explain, not technically a component
parser_explain = subparsers.add_parser("explain", epilog=epilog)
parser_explain.add_argument("explain",
                    help="component to show explain file for",
                    choices=["lyrics","organize","cover"])

def main():
  args = parser.parse_args()
  if args.debug:
    print("~ dbg: ", args)

  component = None
  match args.component:
    case "lyrics":
      component = LyricComponent(args)
    case "organize":
      component = SongOrganizer(args)
    case "cover":
      component = CoverPainter(args)
    case "explain":
      component = LyriaExplain(args.explain)

  if not component:
    parser.print_usage()
    exit(1)

  ret = component.run()
  if ret == -1:
    parser.print_usage()
    exit(ret)

if __name__ == "__main__":
  main()
