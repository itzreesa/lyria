#!/usr/bin/env python3

import subprocess
import venv
import sys
import os

def _create_venv(base_path, venv_path):
  print("[lyria] creating venv.", end='\r')
  os.makedirs(venv_path, exist_ok=True)
  venv.create(venv_path, with_pip=True)
  print("[ ok! ")
  subprocess.check_call([os.path.join(venv_path, "bin", "python"), os.path.join(base_path, "lyria.py"), "$lyria_update_venv"])

def install_requirements():
  base_path = os.path.dirname(os.path.realpath(__file__))
  venv_path = os.path.join(base_path, "venv")

  print("[lyria] updating venv.", end='\r')

  req_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
  subprocess.check_call([os.path.join(venv_path, 'bin', 'pip'), 'install', '--upgrade', '-r', req_file])
  
  print("[ ok! ] updating venv.")
  print("~ lyria is now ready to use!")

def enter_venv():
  base_path = os.path.dirname(os.path.realpath(__file__))
  venv_path = os.path.join(base_path, "venv")
  if not os.path.exists(venv_path):
    _create_venv(base_path, venv_path)
    return
  try:
    subprocess.check_call([os.path.join(venv_path, "bin", "python"), base_path] + sys.argv[1:])
  except:
    pass
  exit(0)

def _download_file(url, dest):
  import urllib.request
  import shutil

  print("~ ... ~ download newest tarball", end='\r')
  with urllib.request.urlopen(url) as res:
    with open(dest, "wb") as out:
      shutil.copyfileobj(res, out)
  print("~ ok!")

def _extract(source, dest):
  print("~ ... ~ extract tarball", end='\r')
  cmd = [
    "tar", "-xzf", source, "--strip-components=1", "-C", dest
  ]
  subprocess.run(cmd, check=True)
  print("~ ok!")

def _chmod(file,):
  import platform
  import stat
  if platform.system() == "Windows":
    return
  print("~ ... ~ chmod executable", end='\r')
  os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)
  print("~ ok!")

def _relink(target, source):
  print("~ ... ~ linking executable", end='\r')
  if os.path.exists(source):
    os.remove(source)
  os.symlink(target, source)
  print("~ ok!")

def update_lyria():
  import requests
  import tempfile
  from components.common import LYRIA_VERSION_FRIENDLY, LYRIA_VERSION_MAJOR, LYRIA_VERSION_MINOR, LYRIA_VERSION_PATCH
  TAGS_URL = "https://api.github.com/repos/itzreesa/lyria/tags"
  res = requests.get(url=TAGS_URL)
  if res.status_code != 200:
    print("[error] can't fetch tags!")
    exit(1)
  data = res.json()
  if not len(data) > 0:
    print("[error] api error. (response len == 0)")
    exit(1)
  if not "name" in data[0]:
    print("[error] api error. ('name' not in data[0])")
    exit(1)

  is_newer = False

  current_tag = f"v{LYRIA_VERSION_FRIENDLY}"
  newest_tag = data[0]["name"]
  
  tag = data[0]["name"][1:].split('.')
  if int(tag[0]) > LYRIA_VERSION_MAJOR:
    is_newer = True
  if int(tag[1]) > LYRIA_VERSION_MINOR:
    is_newer = True
  if int(tag[2]) > LYRIA_VERSION_PATCH:
    is_newer = True
    
  if not is_newer:
    print(f"~ up to date")
    exit(1)
  
  print(f"~ {current_tag} => {newest_tag}, updating!")
  
  LYRIA_DIR = os.path.join(os.getenv("HOME"), ".local", "share", "lyria")
  BIN_DIR = os.path.join(os.getenv("HOME"), ".local", "bin")
  TARBALL_URL = data[0]["tarball_url"]

  os.makedirs(LYRIA_DIR, exist_ok=True)
  os.makedirs(BIN_DIR, exist_ok=True)

  with tempfile.NamedTemporaryFile(delete=False, suffix='.tar.gz') as temp_file:
    _download_file(TARBALL_URL, temp_file.name)
    _extract(temp_file.name, LYRIA_DIR)
    _chmod(os.path.join(LYRIA_DIR, "lyria.py"))
    _relink(os.path.join(LYRIA_DIR, "lyria.py"), os.path.join(BIN_DIR, "lyria"))
  print(f"~ lyria was updated!")

if len(sys.argv) > 1:
  if sys.argv[1] == "$lyria_update_venv":
    install_requirements()
    exit(0)
  elif sys.argv[1] == "update":
    update_lyria()
    install_requirements()
    exit(0)

if __name__ == "__main__":
  enter_venv()