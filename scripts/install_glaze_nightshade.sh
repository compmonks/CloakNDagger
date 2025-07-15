#!/usr/bin/env bash
# Script to download and install Glaze and Nightshade.
# These tools are developed by the University of Chicago SAND Lab.
# They protect artworks by applying perturbations that interfere with AI training.
#
# Usage: ./install_glaze_nightshade.sh [install_directory]
# If no directory is provided, dependencies are installed under 'deps/'.
set -e

INSTALL_DIR="${1:-deps}"

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Clone and install Glaze
if [ ! -d "glaze" ]; then
    echo "Cloning Glaze repository..."
    git clone https://github.com/SAND-Lab/Glaze.git glaze
fi
cd glaze
pip install -e .
cd ..

# Clone and install Nightshade
if [ ! -d "nightshade" ]; then
    echo "Cloning Nightshade repository..."
    git clone https://github.com/SAND-Lab/nightshade.git nightshade
fi
cd nightshade
pip install -e .
cd ..

cat <<MSG
Installation complete.
Glaze and Nightshade have been installed in: $INSTALL_DIR
MSG
