import sys
import os

# find path to root directory of the project so as to import from other packages
# print('current script: visualizer/test_imdb_toy_dataset.py')
# print('os.path.abspath(__file__) = ', os.path.abspath(__file__))
tokens = os.path.abspath(__file__).split('/')
# print('tokens = ', tokens)
path2root = '/'.join(tokens[:-2])
# print('path2root = ', path2root)
if path2root not in sys.path:
    sys.path.append(path2root)

from storage.builtin_datasets import BuiltinDatasetsManager

connector = None  # no connection needed for this file-base datasets
params = None  # no parameter defined for now

data_manager = BuiltinDatasetsManager(connector, params)

# adding builtin/existing datasets
# data_manager.add_dataset('bbc_islam_groups', 'BBC Islam Groups',
#                         '%s/datasets/preprocessed/bbc_islam_groups.json' % path2root)
# data_manager.add_dataset('911_hijackers', '911 Hijackers',
#                         '%s/datasets/preprocessed/911_hijackers.json' % path2root)
# data_manager.add_dataset('enron', 'Enron Email Network',
#                         '%s/datasets/preprocessed/enron.json' % path2root)
# data_manager.add_dataset('moreno_crime', 'Moreno Crime Network',
#                         '%s/datasets/preprocessed/moreno_crime.json' % path2root)
#
# data_manager.add_dataset('imdb', 'IMDB',
#                         '%s/datasets/preprocessed/imdb.json' % path2root)

# data_manager.add_dataset('baseball_steroid_use', 'Baseball Steorid Use',
#                         '%s/datasets/preprocessed/baseball_steroid_use.json' % path2root)

# data_manager.add_dataset('madoff', 'Madoff fraud',
#                         '%s/datasets/preprocessed/madoff.json' % path2root)

# data_manager.add_dataset('montreal_gangs', 'Montreal Street Gangs',
#                         '%s/datasets/preprocessed/montreal_gangs.json' % path2root)

# data_manager.add_dataset('noordintop', 'Noordin Top',
#                         '%s/datasets/preprocessed/noordintop.json' % path2root)

data_manager.add_dataset('rhodes_bombing', 'Rhodes Bombing',
                         '%s/datasets/preprocessed/rhodes_bombing.json' % path2root)


# get available networks
# networks = data_manager.search_networks()
# for g in networks['found']:
#     print(g)

# get a network:
# g = data_manager.get_network('bbc_islam_groups')

# get a sub-network in a network
# g = data_manager.get_network('moreno_crime', node_ids=['person_0', 'person_1', 'crime_0', 'crime_5'])
# print(g)


# get a sub-network in a network
# g = data_manager.get_network('moreno_crime', node_ids=['person_0', 'person_1', 'crime_0', 'crime_5'])
# print(g)

# get list of all nodes in a network
# nodes = data_manager.search_nodes(node_ids=None,network='bbc_islam_groups')
# print(nodes)


# get neighbors of a list of nodes:
neighbors = data_manager.get_neighbors(node_ids=['Christodoulos_Xiros', 'Vassilis Xiros', 'Savas_Xiros'], network='rhodes_bombing')
print(neighbors)
edges = data_manager.get_edges(node_ids=['Christodoulos_Xiros', 'Vassilis Xiros', 'Savas_Xiros'], network='rhodes_bombing')
print(edges)
