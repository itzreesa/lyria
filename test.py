#!/usr/bin/env python3 

import unittest

from components.organize import SongOrganizer
from components.common import extract_tags

# shared test data
FILE_DATA = {
  "artist": ["artist nya", "awh"],
  "album": ["sonic", "crystal"],
  "title": ["tails", "missed"]
}

class ARGS:
  def __init__(self):
    self.artist = None
    self.album = "tails"
    self.path = "collection/"

# tests
class ExtractTest(unittest.TestCase):
  def test_extract_a(self):
    ret = extract_tags(FILE_DATA, ARGS())
    self.assertEqual(ret, ("artist nya", "tails", "tails"))

class OrganizeTest(unittest.TestCase):
  def test_location(self):
    so = SongOrganizer(None, ARGS())
    ret = so._get_location(FILE_DATA, ".flac")
    self.assertEqual(ret, ("collection/artist nya", "tails.flac"))

if __name__ == "__main__":
  unittest.main()