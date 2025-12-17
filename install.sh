#!/bin/sh

LYRIA_DIR="$HOME/.local/share/lyria"
BIN_DIR="$HOME/.local/bin"
TARBALL_URL="https://github.com/itzreesa/lyria/tarball/main/"
TARBALL_LOC=$(mktemp)

mkdir -p "$LYRIA_DIR"
mkdir -p "$BIN_DIR"

curl -L "$TARBALL_URL" -o "$TARBALL_LOC"

tar -xzf "$TARBALL_LOC" -C "$LYRIA_DIR" --strip-components=1

chmod +x "$LYRIA_DIR/lyria.py"

ln -sf "$LYRIA_DIR/lyria.py" "$BIN_DIR/lyria"

rm -f "$TARBALL_LOC"

echo " ~ lyria is now installed!"
echo "if you can't do 'lyria -h', check if '~/.local/bin' is in your 'PATH'"