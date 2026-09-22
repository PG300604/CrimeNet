import os
import sys

# find path to root directory of the project so as to import from other packages
# print('current script: visualizer/test_imdb_toy_dataset.py')
from pathlib import Path
path2root = str(Path(os.path.abspath(__file__)).parents[1])
if path2root not in sys.path:
    sys.path.append(path2root)

from analyzer import request_taker

info = request_taker.get_info()
print(info)
