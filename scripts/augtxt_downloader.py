#!/usr/bin/env python3
import os
from pathlib import Path
import argparse


if __name__ == '__main__':
    # parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", type=str, help="language code")
    parser.add_argument(
        "--fasttext", action='store_true', help=(
            "flag if a pretrained fasttext embedding is to be downloaded. "
            "Example: `python scripts/downloader.py --fasttext --lang=de` "))
    args = parser.parse_args()

    # default folder
    MAINPATH = f"{str(Path.home())}/augtxt_data"

    # Download a fasttext model
    # see https://fasttext.cc/docs/en/unsupervised-tutorial.html
    if args.fasttext and args.lang:
        PATH = f"{MAINPATH}/fasttext"
        URL = "https://dl.fbaipublicfiles.com/fasttext/vectors-wiki"
        ZIPFILE = f"wiki.{args.lang}.zip"
        os.makedirs(PATH, exist_ok=True)
        os.system(f"wget -O '{PATH}/{ZIPFILE}' '{URL}/{ZIPFILE}'")
        os.system(f"unzip -o -d '{PATH}' '{PATH}/{ZIPFILE}'")
        os.system(f"rm '{PATH}/{ZIPFILE}'")

    if args.fasttext:
        print("\nfastext embeddings and vocabulary:", end="")
        os.system(f"ls -lh {MAINPATH}/fasttext" + "| awk '{print $5,$9}' ")
