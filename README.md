# CloakNDagger

An AI cloaking, poisoning and watermarking pipeline to protect your digital content.

## Scripts

Two helper scripts are included in the `scripts/` directory:

* `install_glaze_nightshade.sh` – downloads and installs the [Glaze](https://github.com/SAND-Lab/Glaze) and [Nightshade](https://github.com/SAND-Lab/nightshade) projects. They are required for cloaking and poisoning images.
* `decipher_watermark.py` – deciphers simple LSB-based watermarks from images.

Run `./scripts/install_glaze_nightshade.sh` to clone and install the dependencies. Run `./scripts/decipher_watermark.py <image>` to decode a watermark from an image file.

## Dependencies

* Python 3 with `numpy` and `Pillow` for the watermark decipher script.
* `git` and `pip` to install Glaze and Nightshade.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

The `pipeline` module processes a file by applying Glaze and Nightshade (external
scripts) and embedding an invisible watermark. Paths to your Glaze and
Nightshade scripts should be configured at the top of `src/pipeline.py`.

Run the pipeline for a given file:

```bash
python -m src.pipeline <path-to-file>
```

## Running Tests

```bash
pytest
```