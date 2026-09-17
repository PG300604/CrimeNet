"""
Initialize BuiltinDatasetsManager
"""
import os
from pathlib import Path
from storage.builtin_datasets import BuiltinDatasetsManager  # remove .. to import from root
from .config import config

main_dir = Path(os.path.abspath(__file__)).parents[2]

data_manager = BuiltinDatasetsManager(None, None)

if config.get("datasets"):
    for dataset in config["datasets"]:
        data_manager.add_dataset(dataset["id"], dataset["name"], main_dir / dataset["path"])
