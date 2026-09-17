"""
Set up configurations
"""
from pathlib import Path
from os.path import abspath, dirname
from yaml import load, Loader

config = None

current_dir = Path(dirname(abspath(__file__)))

try:
    with open(current_dir.parent / "settings.yaml") as f:
        config = load(f, Loader=Loader)
except FileNotFoundError:
    raise RuntimeError("settings.yaml was not found!")

if not config.get("temp_file_folder"):
    config["temp_file_folder"] = current_dir.parent.parent / "serve/temp/"
