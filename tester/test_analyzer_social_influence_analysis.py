import os
import sys

# find path to root directory of the project so as to import from other packages
# print('current script: visualizer/test_imdb_toy_dataset.py')
# print('os.path.abspath(__file__) = ', os.path.abspath(__file__))


from pathlib import Path
path2root = str(Path(os.path.abspath(__file__)).parents[1])
if path2root not in sys.path:
    sys.path.append(path2root)

from storage.builtin_datasets import BuiltinDatasetsManager
from analyzer.request_taker import InMemoryAnalyzer


def test_social_influence_analysis():
    connector = None  # no connection needed for this file-base datasets
    params = None  # no parameter defined for now

    data_manager = BuiltinDatasetsManager(connector, params)

    # adding builtin/existing datasets
    data_manager.add_dataset('bbc_islam_groups', 'BBC Islam Groups',
                             '%s/datasets/preprocessed/bbc_islam_groups.json' % path2root)
    data_manager.add_dataset('911_hijackers', '911 Hijackers',
                             '%s/datasets/preprocessed/911_hijackers.json' % path2root)
    data_manager.add_dataset('enron', 'Enron Email Network',
                             '%s/datasets/preprocessed/enron.json' % path2root)
    data_manager.add_dataset('moreno_crime', 'Moreno Crime Network',
                             '%s/datasets/preprocessed/moreno_crime.json' % path2root)

    data_manager.add_dataset('imdb', 'IMDB',
                             '%s/datasets/preprocessed/imdb.json' % path2root)

    network = data_manager.get_network('911_hijackers')
    # define task for testing
    task_id = "social_influence_analysis"
    task_options = {
        # "method": "pagerank",
        # "method": "authority",
        # "method": "betweenness",
        # "method": "closeness_centrality",
        "method": "katz_centrality",
        "parameters": {}
    }

    task = {"task_id": task_id,
            "network": network,
            "options": task_options}

    # call analyzer
    analyzer = InMemoryAnalyzer()
    result = analyzer.perform_analysis(task=task, params=None)
    print('result = ', result)


if __name__ == '__main__':
    test_social_influence_analysis()
