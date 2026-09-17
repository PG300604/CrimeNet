"""
Manage graph database
"""
from .config import config
from .graph import data_manager

if not config["auth_traversal"] in data_manager.datasets:  # create temp data file to init Builtindataset
    data_manager.add_dataset(config["auth_traversal"], "Authentication graph", "", from_file=False)

auth_dataset = data_manager.datasets[config["auth_traversal"]]["data"]
