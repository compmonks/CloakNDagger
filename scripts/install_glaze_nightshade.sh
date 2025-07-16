#!/usr/bin/env bash
# Script to download Glaze and Nightshade.
# These tools are developed by the University of Chicago SAND Lab and
# protect artworks by applying perturbations that interfere with AI training.
#
# Usage: ./install_glaze_nightshade.sh [install_directory]
# If no directory is provided, dependencies are installed under 'deps/'.
set -e

INSTALL_DIR="${1:-deps}"

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Determine URLs based on OS
OS="$(uname)"
case "$OS" in
    Darwin*)
        GLAZE_URL="https://mirror.cs.uchicago.edu/fawkes/files/glaze/Glaze-2.1-arm64.dmg"
        NIGHTSHADE_URL="https://mirror.cs.uchicago.edu/fawkes/files/nightshade/Nightshade-1.0.2-m1.dmg"
        ;;
    MINGW*|MSYS*|CYGWIN*|Windows_NT)
        GLAZE_URL="https://mirror.cs.uchicago.edu/fawkes/files/glaze/Glaze-2.1-Windows.zip"
        NIGHTSHADE_URL="https://mirror.cs.uchicago.edu/fawkes/files/nightshade/Nightshade-1.0-Windows.zip"
        ;;
    *)
        echo "Unsupported OS. Please download manually:" >&2
        echo "  Glaze: https://glaze.cs.uchicago.edu/downloads.html" >&2
        echo "  Nightshade: https://nightshade.cs.uchicago.edu/downloads.html" >&2
        exit 1
        ;;
esac

# Download archives
for URL in "$GLAZE_URL" "$NIGHTSHADE_URL"; do
    FILE="$(basename "$URL")"
    if [ ! -f "$FILE" ]; then
        echo "Downloading $FILE..."
        curl -L -o "$FILE" "$URL"
    else
        echo "$FILE already exists, skipping download"
    fi
done

cat <<MSG
Downloads complete. The archives are located in: $INSTALL_DIR
Refer to the official pages for installation instructions:
  Glaze: https://glaze.cs.uchicago.edu/downloads.html
  Nightshade: https://nightshade.cs.uchicago.edu/downloads.html
MSG
