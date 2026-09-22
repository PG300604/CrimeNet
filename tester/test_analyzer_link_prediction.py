import os
import sys

# find path to root directory of the project so as to import from other packages
path_root_dir = os.path.join(os.path.dirname(__file__), os.path.pardir)
if path_root_dir not in sys.path:
    sys.path.append(path_root_dir)

from storage.builtin_datasets import BuiltinDatasetsManager
from analyzer.request_taker import InMemoryAnalyzer


def test_link_prediction():
    data_manager = BuiltinDatasetsManager(None, None)
    data_manager.add_dataset('moreno_crime', 'Moreno Crime', os.path.join(path_root_dir, 'datasets', 'preprocessed', 'moreno_crime.json'))
    network = data_manager.get_network(network='moreno_crime')

    test_network = {"edges": network.get('edges')[:1000], "nodes": network.get('nodes')[:1000]}

    # define task for testing
    task_id = "link_prediction"
    task_options = {
        # "method": "resource_allocation_index",
        "method": "jaccard_coefficient",
        # "method": "adamic_adar_index",
        # "method": "preferential_attachment",
        # "method": "count_number_soundarajan_hopcroft",
        # "method": "resource_allocation_index_soundarajan_hopcroft",
        # "method": "within_inter_cluster",
        "parameters": {
            # "community_detection_method": 'modularity',
            # "community_detection_method": 'asyn_lpa',
            # "community_detection_method": 'label_propagation',
            "sources": ['crime_466', 'crime_451', 'crime_258'],
            "top_k": 5
        }
    }

    task = {"task_id": task_id,
            "network": test_network,
            "options": task_options}

    # call analyzer
    analyzer = InMemoryAnalyzer()
    result = analyzer.perform_analysis(task=task, params=None)
    print('result = ', result)


if __name__ == '__main__':
    test_link_prediction()
