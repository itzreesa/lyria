from pathlib import Path
import sys

LYRIA_VERSION_MAJOR = 1
LYRIA_VERSION_MINOR = 3
LYRIA_VERSION_PATCH = 2

LYRIA_VERSION_FRIENDLY = f"{LYRIA_VERSION_MAJOR}.{LYRIA_VERSION_MINOR}.{LYRIA_VERSION_PATCH}"

class Color:
  RESET='\033[1;0m'
  SUCCESS='\033[1;32m'
  WARN='\033[1;33m'
  FAIL='\033[1;31m'
  BOLD='\033[1m'
  STATS='\033[36m'

def progress_print(args, ret: int, file: Path):
  if args.silent:
    return
  sys.stdout.write("\r\033[K")

  if args.verbose:
    file = file.absolute()

  match ret:
    case 0:
      print(f" ~ {Color.SUCCESS}success{Color.RESET} ~", file)
    case 1:
      print(f" ~ {Color.FAIL}fail{Color.RESET} ~", file)

    case 2:
      if args.verbose:
        print(f" ~ {Color.FAIL}fail/invalid{Color.RESET} ~", file)
    case 3:
      print(f" ~ {Color.FAIL}fail/fetch{Color.RESET} ~", file)
    case 4:
      print(f" ~ {Color.FAIL}fail/fetch-blank{Color.RESET} ~", file)
    case 5:
      print(f" ~ {Color.FAIL}fail/empty{Color.RESET} ~", file)
    case 6:
      if args.verbose:
        print(f" ~ {Color.FAIL}fail/move{Color.RESET} ~", file)
    case 7:
      print(f" ~ {Color.FAIL}fail/unsupported{Color.RESET} ~", file)

    case 11:
      if args.verbose:
        print(f" ~ {Color.WARN}skip/exists{Color.RESET} ~", file)
    case 12:
      print(f" ~ {Color.WARN}skip/INSTRUMENTAL{Color.RESET} ~", file)
    case 13:
      print(f" ~ {Color.WARN}skip/blank{Color.RESET} ~", file)
      

    case _:
      print(" ~ fail ~", file)