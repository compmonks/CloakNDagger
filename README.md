# CloakNDagger

An AI cloaking, poisoning and watermarking pipeline to protect your digital content.

## Scripts

Two helper scripts are included in the `scripts/` directory:

* `install_glaze_nightshade.sh` – downloads the Glaze and Nightshade binaries from the University of Chicago SAND Lab mirrors. The script selects the proper archive for Windows or macOS and saves it under `deps/`. After downloading, run the installers manually as described on the [Glaze](https://glaze.cs.uchicago.edu/downloads.html) and [Nightshade](https://nightshade.cs.uchicago.edu/downloads.html) pages. These tools are required for cloaking and poisoning images.
* `decipher_watermark.py` – deciphers simple LSB-based watermarks from images.

Run `./scripts/install_glaze_nightshade.sh` to download the archives. Run `./scripts/decipher_watermark.py <image>` to decode a watermark from an image file.

## Dependencies

* Python 3 with `numpy` and `Pillow` for the watermark decipher script.
* `curl` or `wget` to download the Glaze and Nightshade archives.

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