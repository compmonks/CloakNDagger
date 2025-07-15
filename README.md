# CloakNDagger

An AI cloaking, poisoning and watermarking pipeline to protect your digital content.

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
