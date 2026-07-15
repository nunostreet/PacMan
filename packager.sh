#!/usr/bin/env bash
# Builds the Linux executable and packages it as pacman-linux.zip.
# Run this script on a Linux machine — PyInstaller always builds
# for the OS it runs on, so a Mac machine would produce a Mac binary.
#
# The zip extracts to a flat folder so the user can run ./pac-man
# directly from the extracted directory and all relative asset paths resolve.
#
# Usage: bash packager.sh

set -euo pipefail

# Always work from the repo root regardless of where the script is called from
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${ROOT_DIR}"

OUTPUT="pacman-linux.zip"
STAGING="dist/staging"

echo "[packager] Building with PyInstaller..."
venv/bin/pyinstaller pac-man.spec --noconfirm

# Create a staging folder with everything at the same level so that
# running ./pac-man from the extracted directory resolves assets/ correctly
echo "[packager] Staging files..."
rm -rf "${STAGING}"
mkdir -p "${STAGING}"

# The compiled binary
cp dist/pac-man "${STAGING}/pac-man"

# Assets and config must be next to the binary — game loads them with
# relative paths like "assets/..." so they must be in the working directory
cp -r assets/ "${STAGING}/assets/"
cp -r config/ "${STAGING}/config/"
cp README.txt "${STAGING}/README.txt"

echo "[packager] Creating ${OUTPUT}..."
rm -f "${OUTPUT}"
# Zip from inside staging so paths inside the zip are clean (no dist/staging/ prefix)
cd "${STAGING}"
zip -r "../../${OUTPUT}" . --exclude "__pycache__/*"
cd "${ROOT_DIR}"

# Clean up staging folder
rm -rf "${STAGING}"

echo "[packager] Done: ${OUTPUT}"
echo "[packager] Contents:"
unzip -l "${OUTPUT}"
