import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np
from PIL import Image


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "decipher_watermark.py"
SPEC = importlib.util.spec_from_file_location("decipher_watermark", SCRIPT_PATH)
DECODER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DECODER)


class DecodeLsbTests(unittest.TestCase):
    def test_decodes_null_terminated_ascii_message(self):
        payload = b"CloakNDagger\x00"
        bits = np.unpackbits(np.frombuffer(payload, dtype=np.uint8))
        pixels = np.zeros((1, len(bits), 3), dtype=np.uint8)
        pixels.reshape(-1)[: len(bits)] = bits

        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = Path(temp_dir) / "watermarked.png"
            Image.fromarray(pixels, mode="RGB").save(image_path)

            self.assertEqual(DECODER.decode_lsb(image_path), "CloakNDagger")


if __name__ == "__main__":
    unittest.main()
