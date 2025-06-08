import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


list_of_files = [
    ""
]


logging.basicConfig(level=logging.INFO)

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir = filepath.parent
    filename = filepath.name

    # Create the directory if it doesn't exist
    if filedir != Path("."):
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for the file: {filename}")

    # Create empty file if it doesn't exist or is 0 bytes
    if (not filepath.exists()) or (filepath.stat().st_size == 0):
        with open(filepath, "w") as f:
            pass
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filename} already exists")