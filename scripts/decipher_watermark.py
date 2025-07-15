#!/usr/bin/env python3
"""Simple script to decipher LSB-based image watermarks.

This script is an example of how to decode a watermark that has been hidden in
an image using the least significant bit (LSB) method. It expects a PNG or JPG
file and outputs the decoded message on stdout.
"""
import argparse
from PIL import Image
import numpy as np

def decode_lsb(image_path: str) -> str:
    img = Image.open(image_path)
    data = np.array(img)
    # Extract the least significant bit of each pixel channel
    bits = data & 1
    flat = bits.flatten()
    chars = []
    for i in range(0, len(flat), 8):
        byte = flat[i:i+8]
        if len(byte) < 8:
            break
        value = 0
        for bit in byte:
            value = (value << 1) | int(bit)
        if value == 0:
            break
        chars.append(chr(value))
    return ''.join(chars)


def main():
    parser = argparse.ArgumentParser(description="Decipher LSB watermark")
    parser.add_argument("image", help="Path to the watermarked image")
    args = parser.parse_args()
    message = decode_lsb(args.image)
    print(message)

if __name__ == "__main__":
    main()
