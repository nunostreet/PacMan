#!/usr/bin/env bash
# Builds the Linux executable and packages it as pacman-linux.zip.
# Run this script on a Linux machine — PyInstaller always builds
# for the OS it runs on, so a Mac machine would produce a Mac binary.
#
# Usage: bash packager.sh

set -euo pipefail

# Always work from the repo root regardless of where the script is called from
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

OUTPUT="pacman-linux.zip"

# Compile the Python project into a single self-contained binary.
# The spec file (pac-man.spec) tells PyInstaller what to bundle:
# assets, config, and the mazegenerator package.
echo "[packager] Building with PyInstaller..."
venv/bin/pyinstaller pac-man.spec --noconfirm

# Pack the binary together with the files the game expects at runtime:
# - dist/pac-man      the compiled executable
# - config/config.json  game settings (users may want to edit this)
# - assets/           sprites and fonts
# - README.txt        instructions for running the executable
echo "[packager] Creating ${OUTPUT}..."
rm -f "${OUTPUT}"
zip -r "${OUTPUT}" \
    dist/pac-man \
    config/config.json \
    assets/ \
    README.txt \
    --exclude "__pycache__/*"

echo "[packager] Done: ${OUTPUT}"
