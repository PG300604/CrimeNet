import os
import sys

# find path to root directory of the project so as to import from other packages
# print('current script: visualizer/test_imdb_toy_dataset.py')
# print('os.path.abspath(__file__) = ', os.path.abspath(__file__))
tokens = os.path.abspath(__file__).split('/')
# print('tokens = ', tokens)
path2root = '/'.join(tokens[:-2])
# print('path2root = ', path2root)
if path2root not in sys.path:
    sys.path.append(path2root)

from analyzer import request_taker

info = request_taker.get_info()
print(info)
