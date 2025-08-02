import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "coffee-shop-sentiment-analyzer"

list_of_files = [
    ".github/workflows/.gitkeep",
    "data/raw/.gitkeep",
    "data/processed/__init__.py",
    "models/__init__.py",
    "models/__init__.py",
    "notebooks/.gitkeep",
    "src/__init__.py",
    "src/config.py",
    "src/data_preprocessing.py",
    "src/model.py",
    "src/train.py",
    "src/predict.py",
    "tests/__init__.py",
    "tests/test_preprocessing.py",
    "main.py",
    "requirements.txt",
    "README.md",
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")
