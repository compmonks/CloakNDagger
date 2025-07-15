"""Media processing pipeline for Glaze and Nightshade.

This module offers functions to protect images and videos from AI models by
applying Glaze, Nightshade poisoning, and invisible watermarking.
"""

from __future__ import annotations

import logging
import mimetypes
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

import cv2
import numpy as np
import pywt

# ---- USER CONFIG ----
GLAZE_PATH = "/path/to/glaze.py"
NIGHTSHADE_PATH = "/path/to/nightshade.py"
PROMPT = "NFT poison"
WATERMARK = "DreamNFT:0xAbC123...:Token1"

logger = logging.getLogger(__name__)


@dataclass
class VideoPaths:
    temp_frames: Path
    glaze_frames: Path
    nightshade_frames: Path
    watermark_frames: Path


# Utility functions ---------------------------------------------------------


def is_image(file: str | os.PathLike) -> bool:
    """Return ``True`` if ``file`` is an image based on MIME type."""

    mt, _ = mimetypes.guess_type(str(file))
    return mt is not None and mt.startswith("image")


def is_video(file: str | os.PathLike) -> bool:
    """Return ``True`` if ``file`` is a video based on MIME type."""

    mt, _ = mimetypes.guess_type(str(file))
    return mt is not None and mt.startswith("video")


def _ensure_exists(path: str | os.PathLike) -> None:
    if not Path(path).exists():
        raise FileNotFoundError(f"Required path does not exist: {path}")


# Watermarking -------------------------------------------------------------


def embed_watermark(frame: np.ndarray, watermark_bits: str) -> np.ndarray:
    """Embed ``watermark_bits`` into ``frame`` using Haar wavelets."""

    b, g, r = cv2.split(frame)
    coeffs = pywt.dwt2(b, "haar")
    LL, (LH, HL, HH) = coeffs
    flat_LL = LL.flatten()
    for i, bit in enumerate(watermark_bits):
        if i >= len(flat_LL):
            break
        val = int(flat_LL[i])
        val = (val & ~1) | int(bit)
        flat_LL[i] = val
    LL_wm = flat_LL.reshape(LL.shape)
    b_wm = pywt.idwt2((LL_wm, (LH, HL, HH)), "haar")
    b_wm = np.uint8(np.clip(b_wm, 0, 255))
    return cv2.merge([b_wm, g, r])


# Image processing ---------------------------------------------------------


def process_image(file: str) -> Path:
    """Apply Glaze, Nightshade, and watermark to ``file``."""

    _ensure_exists(file)
    basename = os.path.basename(file)
    glazed = Path(f"glaze_{basename}")
    nightshade = Path(f"ns_{basename}")
    watermarked = Path(f"wm_{basename}")

    logger.debug("Glazing %s", file)
    subprocess.run(
        [sys.executable, GLAZE_PATH, "--input", file, "--output", glazed], check=True
    )

    logger.debug("Applying Nightshade to %s", glazed)
    subprocess.run(
        [
            sys.executable,
            NIGHTSHADE_PATH,
            "--input",
            glazed,
            "--output",
            nightshade,
            "--prompt",
            PROMPT,
        ],
        check=True,
    )

    logger.debug("Embedding watermark into %s", nightshade)
    img = cv2.imread(str(nightshade))
    wm_bits = "".join(format(ord(c), "08b") for c in WATERMARK)
    img_wm = embed_watermark(img, wm_bits)
    cv2.imwrite(str(watermarked), img_wm)
    logger.info("Processed image written to %s", watermarked)
    return watermarked


# Video processing ---------------------------------------------------------


def _make_video_paths(base: Path) -> VideoPaths:
    return VideoPaths(
        temp_frames=base / "tmp_frames",
        glaze_frames=base / "tmp_glaze",
        nightshade_frames=base / "tmp_ns",
        watermark_frames=base / "tmp_wm",
    )


def process_video(file: str) -> Path:
    """Apply Glaze, Nightshade, and watermark to video ``file``."""

    _ensure_exists(file)
    base = Path(".")
    paths = _make_video_paths(base)
    for p in paths.__dict__.values():
        p.mkdir(parents=True, exist_ok=True)

    vidcap = cv2.VideoCapture(file)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frames: List[Path] = []
    i = 0
    while True:
        ret, frame = vidcap.read()
        if not ret:
            break
        fpath = paths.temp_frames / f"frame_{i:06d}.png"
        cv2.imwrite(str(fpath), frame)
        frames.append(fpath)
        i += 1
    vidcap.release()

    glazed: List[Path] = []
    for idx, f in enumerate(frames):
        out = paths.glaze_frames / f"frame_{idx:06d}.png"
        subprocess.run(
            [sys.executable, GLAZE_PATH, "--input", f, "--output", out], check=True
        )
        glazed.append(out)

    poisoned: List[Path] = []
    for idx, f in enumerate(glazed):
        out = paths.nightshade_frames / f"frame_{idx:06d}.png"
        subprocess.run(
            [
                sys.executable,
                NIGHTSHADE_PATH,
                "--input",
                f,
                "--output",
                out,
                "--prompt",
                PROMPT,
            ],
            check=True,
        )
        poisoned.append(out)

    wm_bits = "".join(format(ord(c), "08b") for c in WATERMARK)
    wmed: List[Path] = []
    for idx, f in enumerate(poisoned):
        img = cv2.imread(str(f))
        img_wm = embed_watermark(img, wm_bits)
        out = paths.watermark_frames / f"frame_{idx:06d}.png"
        cv2.imwrite(str(out), img_wm)
        wmed.append(out)

    frame0 = cv2.imread(str(wmed[0]))
    h, w, _ = frame0.shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    outvid = Path("final_output.mp4")
    out = cv2.VideoWriter(str(outvid), fourcc, fps, (w, h))
    for f in wmed:
        out.write(cv2.imread(str(f)))
    out.release()
    logger.info("Processed video written to %s", outvid)
    return outvid


# CLI ----------------------------------------------------------------------


def main(argv: List[str] | None = None) -> None:
    """Run the pipeline for the file specified in ``argv``."""

    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m pipeline <yourfile>")
        return

    file = argv[0]
    if is_image(file):
        logger.info("Detected image.")
        process_image(file)
    elif is_video(file):
        logger.info("Detected video.")
        process_video(file)
    else:
        logger.warning(
            "File type not supported for Glaze/Nightshade/watermarking yet. You can still encrypt it for NFT access."
        )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
