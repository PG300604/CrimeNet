import os
import sys

# find path to root directory of the project so as to import from other packages
# print('current script: visualizer/test_imdb_toy_dataset.py')
from pathlib import Path
path2root = str(Path(os.path.abspath(__file__)).parents[1])
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
                             f'{path2root}/datasets/preprocessed/montreal_gangs.json')
    data_manager.add_dataset('noordintop', 'Noordin Top',
                             f'{path2root}/datasets/preprocessed/noordintop.json')
    data_manager.add_dataset('rhodes_bombing', 'Rhodes Bombing',
                             f'{path2root}/datasets/preprocessed/rhodes_bombing.json')
    data_manager.add_dataset('moreno_crime', 'Moreno Crime Network',
                             f'{path2root}/datasets/preprocessed/moreno_crime.json')

    network = data_manager.get_network(network='moreno_crime')

    # define task for testing
    task_id = "node_embedding"
    task_options = {
        "method": "deepwalk",
        "parameters": {
            "K": 32
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
