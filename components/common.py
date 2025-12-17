def extract_tags(file_data, args) -> tuple:
  artist = file_data["artist"][0]
  album = ""
  if "album" in file_data:
    album = file_data["album"][0]
  title = file_data["title"][0]

  if args.artist:
    artist = args.artist
  if args.album:
    album = args.album

  # sanitize!
  if "/" in artist:
    artist = artist.replace("/", " ")
  if "/" in title:
    title = title.replace("/", " ")

  return artist, album, title