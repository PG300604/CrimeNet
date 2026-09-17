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

from storage.toy_datasets.toy_data_manager import ToyDataManager
from storage.builtin_datasets import BuiltinDatasetsManager
from analyzer.request_taker import InMemoryAnalyzer


def test_node_embedding():
    # data_manager = ToyDataManager(connector=None, params=None)
    connector = None  # no connection needed for this file-base datasets
    params = None  # no parameter defined for now
    data_manager = BuiltinDatasetsManager(connector, params)

    data_manager.add_dataset('montreal_gangs', 'Montreal Street Gangs',
                             '%s/datasets/preprocessed/montreal_gangs.json' % path2root)
    data_manager.add_dataset('noordintop', 'Noordin Top',
                             '%s/datasets/preprocessed/noordintop.json' % path2root)
    data_manager.add_dataset('rhodes_bombing', 'Rhodes Bombing',
                             '%s/datasets/preprocessed/rhodes_bombing.json' % path2root)
    data_manager.add_dataset('imdb', 'IMDB',
                             '%s/datasets/preprocessed/imdb.json' % path2root)
    data_manager.add_dataset('moreno_crime', 'Moreno Crime Network',
                             '%s/datasets/preprocessed/moreno_crime.json' % path2root)

    network = data_manager.get_network(network='moreno_crime')

    # define task for testing
    task_id = "node_embedding"
    task_options = {
        # "method": "svd",
        # "method": "nmf",
        # "method": "deepwalk",
        # "method": "node2vec",
        "method": "line",
        # "method": "sine",
        # "method": "role2vec",
        "parameters": {
            "K": 128
        }
    }

    task = {"task_id": task_id,
            "network": network,
            "options": task_options}

    # call analyzer
    analyzer = InMemoryAnalyzer()
    result = analyzer.perform_analysis(task=task, params=None)
    # print('result = ', result)
    print('len of vectors = ', len(result['vectors']))


if __name__ == '__main__':
    test_node_embedding()
