import sys
import os
import networkx as nx

# find path to root directory of the project so as to import from other packages
path2root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path2root not in sys.path:
    sys.path.append(path2root)

import analyzer.common.helpers as helpers


def pagerank(network, params):
    """
    wrapper for NetworkX's parerank function
    :param network:
    :param params:

    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'scores': a dictionary of pagerank score of nodes in network
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_directed_graph(network)
        # print(graph)
        # print(node_ids)
        pr = nx.pagerank(graph)
        scores = [(node_ids[i], pr[i]) for i in range(len(node_ids))]
        # print(scores)
        scores = dict(scores)
        result = {'success': 1, 'message': 'the task is performed successfully', 'scores': scores}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'scores': None}
        return result


def authority(network, params):
    """
    wrapper for NetworkX's hits function
    :param network:
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'scores': a dictionary of pagerank score of nodes in network
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_directed_graph(network)
        # print(graph)
        # print(node_ids)
        _, a = nx.hits(graph)
        scores = [(node_ids[i], a[i]) for i in range(len(node_ids))]
        # print(scores)
        scores = dict(scores)
        result = {'success': 1, 'message': 'the task is performed successfully', 'scores': scores}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'scores': None}
        return result


def betweenness(network, params):
    """
    wrapper for NetworkX's betweeness_centrality function
    :param network:
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'scores': a dictionary of pagerank score of nodes in network
        }

    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)  # TODO: to be refactor
        # print(graph)
        # print(node_ids)
        centralities = nx.betweenness_centrality(graph)
        scores = [(node_ids[i], centralities[i]) for i in range(len(node_ids))]
        # print(scores)
        scores = dict(scores)
        result = {'success': 1, 'message': 'the task is performed successfully', 'scores': scores}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'scores': None}
        return result


def katz_centrality(network, params):
    """
    wrapper for NetworkX's katz_centrality function
    :param network:
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'scores': a dictionary of pagerank score of nodes in network
        }

    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)  # TODO: to be refactor
        # print(graph)
        # print(node_ids)
        centralities = nx.katz_centrality(graph)
        scores = [(node_ids[i], centralities[i]) for i in range(len(node_ids))]
        # print(scores)
        scores = dict(scores)
        result = {'success': 1, 'message': 'the task is performed successfully', 'scores': scores}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'scores': None}
        return result


def closeness_centrality(network, params):
    """
    wrapper for NetworkX's closeness_centrality function
    :param network:
    :param params:
     :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'scores': a dictionary of pagerank score of nodes in network
        }

    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)  # TODO: to be refactor
        # print(graph)
        # print(node_ids)
        centralities = nx.katz_centrality(graph)
        scores = [(node_ids[i], centralities[i]) for i in range(len(node_ids))]
        # print(scores)
        scores = dict(scores)
        result = {'success': 1, 'message': 'the task is performed successfully', 'scores': scores}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'scores': None}
        return result


def get_info():
    """
    get information about methods provided in this class
    :return: dictionary: Provides the name of the analysis task, available methods and information
                         about an methods parameter. Also provides full names of tasks, methods and parameter.
                         Information is provided in the following format:

                        {
                            'name': Full analysis task name as string
                            'methods': {
                                key: Internal method name (eg. 'asyn_lpa')
                                value: {
                                    'name': Full method name as string
                                    'parameter': {
                                        key: Parameter name
                                        value: {
                                            'description': Description of the parameter
                                            'fixed_options': {
                                                key: Accepted parameter value
                                                value: Full parameter value name as string
                                                !! If accepted values are integers key and value is 'Integer'. !!
                                            }
                                        }
                                    }
                                }
                            }
                        }
    """
    info = {'name': 'Social Influence Analysis',
            'methods': {
                'pagerank': {
                    'name': 'Pagerank',
                    'parameter': {}
                },
                'authority': {
                    'name': 'Authority',
                    'parameter': {}
                },
                'betweenness': {
                    'name': 'Betweeness Centrality',
                    'parameter': {}
                },
                'closeness_centrality': {
                    'name': 'Closeness Centrality',
                    'parameter': {}
                }
            }
            }
    return info


class SocialInfluenceAnalyzer:
    """
    class for performing community detection
    """

    def __init__(self, algorithm):
        """
        init a community detector using the given `algorithm`
        :param algorithm:
        """
        self.algorithm = algorithm
        self.methods = {
            'pagerank': pagerank,
            'authority': authority,
            'betweenness': betweenness,
            'betweenness_centrality': betweenness,
            'katz_centrality': katz_centrality,
            'katz': katz_centrality,
            'closeness_centrality': closeness_centrality,
            'closeness': closeness_centrality
            # TODO: to add more methods from networkx, snap, and sklearn
        }

    def perform(self, network, params):
        """
        performing
        :param network:
        :param params:
        :return:
        """
        return self.methods[self.algorithm](network, params)
