import numpy as np
import cv2
from src import pipeline


def test_is_image(tmp_path):
    f = tmp_path / "img.png"
    cv2.imwrite(str(f), np.zeros((10, 10, 3), dtype=np.uint8))
    assert pipeline.is_image(str(f))


def test_is_video(tmp_path):
    f = tmp_path / "vid.mp4"
    # Create a tiny video
    out = cv2.VideoWriter(str(f), cv2.VideoWriter_fourcc(*"mp4v"), 1, (2, 2))
    out.write(np.zeros((2, 2, 3), dtype=np.uint8))
    out.release()
    assert pipeline.is_video(str(f))


def test_embed_watermark_preserves_shape():
    img = np.zeros((4, 4, 3), dtype=np.uint8)
    bits = "1010" * 4
    wm = pipeline.embed_watermark(img, bits)
    assert wm.shape == img.shape
