import pickle
import sys
import os

# find path to root directory of the project so as to import from other packages
# to be refactored
# print('current script: storage/toy_datasets/toy_data_manager.py')
from pathlib import Path
path2root = str(Path(os.path.abspath(__file__)).parents[2])
if path2root not in sys.path:
    sys.path.append(path2root)

from framework.interfaces import DataManager
from storage.toy_datasets.enron import EnronDataset
from storage.toy_datasets.moreno_crime import MorenoCrimeDataset


class ToyDataManager(DataManager):
    """

    """

    def __init__(self, connector, params):
        super(ToyDataManager, self).__init__(connector, params)
        self.datasets = {'enron': EnronDataset(connector, {'data_file': 'datasets/enron_dataset.pkl'}),
                         'moreno_crime': MorenoCrimeDataset(connector,
                                                            params={'data_file': 'datasets/moreno_crime_dataset.pkl'})}

    def get_network(self, network, node_ids=None, params=None):
        if network in self.datasets:
            return self.datasets[network].get_network(node_ids=node_ids, params=params)
        else:
            return {'edges': [], 'nodes': []}

    def get_neighbors(self, node_ids, network, params=None):
        if network in self.datasets:
            return self.datasets[network].get_neighbors(node_ids=node_ids, params=params)
        else:
            return {'found': [], 'not_found': node_ids}

    def search_nodes(self, node_ids, network, params=None):
        if network in self.datasets:
            return self.datasets[network].search_nodes(node_ids=node_ids, params=params)
        else:
            return {'found': [], 'not_found': node_ids}
