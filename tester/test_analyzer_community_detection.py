import os
import sys
import json

# find path to root directory of the project so as to import from other packages
# print('current script: visualizer/test_imdb_toy_dataset.py')
from pathlib import Path
path2root = str(Path(os.path.abspath(__file__)).parents[1])
if path2root not in sys.path:
    sys.path.append(path2root)

from storage.toy_datasets.toy_data_manager import ToyDataManager
from analyzer.request_taker import InMemoryAnalyzer
from storage.builtin_datasets import BuiltinDatasetsManager


def test_community_detection():
    data_manager = BuiltinDatasetsManager(None, None)
    network_id = 'moreno_crime'
    data_manager.add_dataset(network_id, 'Moreno Crime', f'{path2root}/datasets/preprocessed/moreno_crime.json')
    network = data_manager.get_network(network=network_id)

    test_network = {"edges": network.get('edges')[:100],
                    "nodes": network.get('nodes')[:100]}

    # define task for testing
    task_id = "community_detection"
    task_options = {
        "method": "modularity",
        # "method": "k_cliques",
        # "method": "spectral",
        # "method": "asyn_lpa",
        # "method": "label_propagation",
        # "method": "bipartition",
        # "method": "hierarchical",
        # 'parameters': {}
        "parameters": {'K': 2}
    }

    task = {"task_id": task_id,
            "network": test_network,
            "options": task_options}

    # call analyzer
    analyzer = InMemoryAnalyzer()
    result = analyzer.perform_analysis(task=task, params=None)
    print(result)

    network_analysis_output_dir = os.path.join(path2root, 'analysis_results') 
    if not os.path.exists(network_analysis_output_dir):
        os.makedirs(network_analysis_output_dir)

    filename_result = '%s_%s_%s.json' % (task_id, task_options['method'], network_id)
    filepath_result = os.path.join(network_analysis_output_dir, filename_result)

    # for key in result.keys():
    #     if type(key) is not str:
    #         try:
    #             result[str(key)] = result[key]
    #         except:
    #             try:
    #                 result[repr(key)] = result[key]
    #             except:
    #                 pass
    #         del result[key]

    with open(filepath_result, 'w') as outfile:
        json.dump(result, outfile, indent=4)
    print('Dumped successfuly:', filepath_result)


# print("communities = ", result[0][0])
# print("membership = ", result[0][1])

if __name__ == '__main__':
    test_community_detection()
