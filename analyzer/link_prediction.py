import sys
import os
import networkx.algorithms.link_prediction as methods
import networkx.algorithms.community as community_methods
from operator import itemgetter

# find path to root directory of the project so as to import from other packages
path2root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path2root not in sys.path:
    sys.path.append(path2root)

import analyzer.common.helpers as helpers


def _get_sources(nx_graph, params, node_index):
    if 'sources' in params:
        sources = params['sources']
        sources = [node_index[u] for u in sources]
    else:
        sources = nx_graph.nodes

    return sources


def _get_candidates(nx_graph, sources):
    """
    find candidate (new) links for a list of nodes.
    Only returns node pairs that do NOT already have an edge in the graph.
    :param nx_graph: networkx graph
    :param sources: list of node ids
    :return: list of (u, v) pairs representing potential/missing links
    """
    candidates = []

    if sources is None:
        sources = nx_graph.nodes

    # Pre-build the existing edge set for O(1) lookup
    existing_edges = set(nx_graph.edges())
    existing_edges_reversed = set((v, u) for u, v in existing_edges)
    all_existing = existing_edges | existing_edges_reversed

    for u in sources:
        # Convert to a set immediately — nx_graph.neighbors() returns an iterator
        # that gets exhausted if iterated, so we must materialise it first
        neighbors_set = set(nx_graph.neighbors(u))
        second_hop_neighbors = set()
        for v in neighbors_set:
            second_hop_neighbors = second_hop_neighbors.union(set(nx_graph.neighbors(v)))

        # Remove direct neighbors AND self from candidates
        second_hop_neighbors -= neighbors_set
        second_hop_neighbors.discard(u)

        # Final safety filter: exclude any pair that already has an edge
        for v in second_hop_neighbors:
            if (u, v) not in all_existing:
                candidates.append((u, v))

    return candidates


def _select_top_k(candidates, k=3):
    candidates.sort(key=itemgetter(1), reverse=True)
    return [u[0] for u in candidates[:k]]


def _generate_link_predictions(scores, params, sources, node_ids):
    preds = dict([(node_ids[u], []) for u in sources])

    for u, v, p in scores:
        # print('(%d, %d) -> %.8f' % (u, v, p))
        preds[node_ids[u]].append((node_ids[v], p))

    for u in preds:
        if 'top_k' in params:
            preds[u] = _select_top_k(preds[u], params['top_k'])
        else:
            preds[u] = _select_top_k(preds[u])

    return preds


def _call_nx_community_detection_method(method_name, graph):
    """
    call networkx' community detection methods. 
    supported methods including 'modularity', 'asyn_lpa', 'label_propagation'
    :param method_name: the name of networkx' community detection algorithm
    :param graph: networkx graph
    :return:
    """
    supported_community_methods = ('modularity', 'asyn_lpa', 'label_propagation')

    if method_name not in supported_community_methods:
        return None

    if method_name is supported_community_methods[0]:
        return community_methods.greedy_modularity_communities(graph)
    elif method_name is supported_community_methods[1]:
        return community_methods.asyn_lpa_communities(graph)
    elif method_name is supported_community_methods[2]:
        return community_methods.label_propagation_communities(graph)
    else:
        return None


def resource_allocation_index(network, params):
    """
    predict links for a set of nodes using networkx' resource_allocation_index function
    :param network: networkx network
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'predictions': predictions
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        node_index = [(node_ids[i], i) for i in range(len(node_ids))]
        node_index = dict(node_index)
        if params is None:
            params = {}

        sources = _get_sources(graph, params, node_index)
        candidates = _get_candidates(graph, sources)
        scores = methods.resource_allocation_index(graph, candidates)
        predictions = _generate_link_predictions(scores, params, sources, node_ids)
        result = {'success': 1, 'message': 'the task is performed successfully', 'predictions': predictions}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'predictions': None}
        return result


def jaccard_coefficient(network, params=None):
    """
    predict links for a set of nodes using networkx' jaccard_coefficient function
    :param network: networkx network
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'predictions': predictions
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        node_index = [(node_ids[i], i) for i in range(len(node_ids))]
        node_index = dict(node_index)
        if params is None:
            params = {}

        sources = _get_sources(graph, params, node_index)
        candidates = _get_candidates(graph, sources)
        scores = methods.jaccard_coefficient(graph, candidates)
        predictions = _generate_link_predictions(scores, params, sources, node_ids)

        result = {'success': 1, 'message': 'the task is performed successfully', 'predictions': predictions}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'predictions': None}
        return result


def adamic_adar_index(network, params):
    """
    predict links for a set of nodes using networkx' adamic_adar_index function
    :param network: networkx network
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'predictions': predictions
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        node_index = [(node_ids[i], i) for i in range(len(node_ids))]
        node_index = dict(node_index)
        if params is None:
            params = {}

        sources = _get_sources(graph, params, node_index)
        candidates = _get_candidates(graph, sources)
        scores = methods.adamic_adar_index(graph, candidates)
        predictions = _generate_link_predictions(scores, params, sources, node_ids)

        result = {'success': 1, 'message': 'the task is performed successfully', 'predictions': predictions}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'predictions': None}
        return result


def preferential_attachment(network, params):
    """
    predict links for a set of nodes using networkx' preferential_attachment function to
    compute the preferential attachment score of all node pairs in network.
    :param network: networkx network
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'predictions': predictions
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        node_index = [(node_ids[i], i) for i in range(len(node_ids))]
        node_index = dict(node_index)
        if params is None:
            params = {}

        sources = _get_sources(graph, params, node_index)
        candidates = _get_candidates(graph, sources)
        scores = methods.preferential_attachment(graph, candidates)
        predictions = _generate_link_predictions(scores, params, sources, node_ids)

        result = {'success': 1, 'message': 'the task is performed successfully', 'predictions': predictions}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'predictions': None}
        return result


def count_number_soundarajan_hopcroft(network, params):
    """
    predict links for a set of nodes using networkx' cn_soundarajan_hopcroft function to 
    count the number of common neighbors
    :param network: networkx network
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'predictions': predictions
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        node_index = [(node_ids[i], i) for i in range(len(node_ids))]
        node_index = dict(node_index)
        if params is None:
            params = {}

        try:
            community_detection_method = params['community_detection_method']
        except Exception as e:
            print('Community detection method is not defined.', e)
            return None

        nx_comms = _call_nx_community_detection_method(community_detection_method, graph)
        if nx_comms is None:
            print("Community detection method is not supported.")
            return None
        else:
            nx_comms = list(nx_comms)

        # initalize community information
        for node in graph.nodes():
            graph.nodes[node]['community'] = None

        # add community information
        for i in range(len(nx_comms)):
            for node in nx_comms[i]:
                if graph.nodes[node]['community'] is None:
                    graph.nodes[node]['community'] = i

        sources = _get_sources(graph, params, node_index)
        candidates = _get_candidates(graph, sources)
        scores = methods.cn_soundarajan_hopcroft(graph, candidates)
        predictions = _generate_link_predictions(scores, params, sources, node_ids)

        result = {'success': 1, 'message': 'the task is performed successfully', 'predictions': predictions}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'predictions': None}
        return result


def resource_allocation_index_soundarajan_hopcroft(network, params):
    """
    predict links for a set of nodes using networkx' ra_index_soundarajan_hopcroft function to 
    compute the resource allocation index of all node pairs in network using community information.
    :param network: networkx network
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'predictions': predictions
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        node_index = [(node_ids[i], i) for i in range(len(node_ids))]
        node_index = dict(node_index)
        if params is None:
            params = {}

        try:
            community_detection_method = params['community_detection_method']
        except Exception as e:
            print('Community detection method is not defined.', e)
            return None

        nx_comms = _call_nx_community_detection_method(community_detection_method, graph)
        if nx_comms is None:
            print("Community detection method is not supported.")
            return None
        else:
            nx_comms = list(nx_comms)

        # initalize community information
        for node in graph.nodes():
            graph.nodes[node]['community'] = None

        # add community information
        for i in range(len(nx_comms)):
            for node in nx_comms[i]:
                if graph.nodes[node]['community'] is None:
                    graph.nodes[node]['community'] = i

        sources = _get_sources(graph, params, node_index)
        candidates = _get_candidates(graph, sources)
        scores = methods.ra_index_soundarajan_hopcroft(graph, candidates)
        predictions = _generate_link_predictions(scores, params, sources, node_ids)

        result = {'success': 1, 'message': 'the task is performed successfully', 'predictions': predictions}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'predictions': None}
        return result


def within_inter_cluster(network, params):
    """
    predict links for a set of nodes using networkx' within_inter_cluster to 
    compute the ratio of within- and inter-cluster common neighbors of all node pairs in network.
    :param network: networkx network
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'predictions': predictions
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        node_index = [(node_ids[i], i) for i in range(len(node_ids))]
        node_index = dict(node_index)
        if params is None:
            params = {}

        try:
            community_detection_method = params['community_detection_method']
        except Exception as e:
            print('Community detection method is not defined.', e)
            return None

        nx_comms = _call_nx_community_detection_method(community_detection_method, graph)
        if nx_comms is None:
            print("Community detection method is not supported.")
            return None
        else:
            nx_comms = list(nx_comms)

        # initalize community information
        for node in graph.nodes():
            graph.nodes[node]['community'] = None

        # add community information
        for i in range(len(nx_comms)):
            for node in nx_comms[i]:
                if graph.nodes[node]['community'] is None:
                    graph.nodes[node]['community'] = i

        sources = _get_sources(graph, params, node_index)
        candidates = _get_candidates(graph, sources)
        scores = methods.within_inter_cluster(graph, candidates)
        predictions = _generate_link_predictions(scores, params, sources, node_ids)

        result = {'success': 1, 'message': 'the task is performed successfully', 'predictions': predictions}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'predictions': None}
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
                                            'options': {
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
    info = {'name': 'Link Prediction',
            'methods': {
                'resource_allocation_index': {
                    'name': 'Resource Allocation Index',
                    'parameter': {}
                },
                'jaccard_coefficient': {
                    'name': 'Jaccard Coefficient',
                    'parameter': {}
                },
                'adamic_adar_index': {
                    'name': 'Adamic Adar Index',
                    'parameter': {}
                },
                'count_number_soundarajan_hopcroft': {
                    'name': 'Soundarajan Hopcroft (Count Numbers)',
                    'parameter': {
                        'community_detection_method': {
                            'description': 'Community detection method',
                            'options': {'modularity': 'Modularity',
                                        'asyn_lpa': 'Asynchronous Label Propagation',
                                        'label_propagation': 'Label Propagation'}
                        }
                    }
                },
                'resource_allocation_index_soundarajan_hopcroft': {
                    'name': 'Resource Alocation Index (Soundarajan Hopcroft)',
                    'parameter': {
                        'community_detection_method': {
                            'description': 'Community detection method',
                            'options': {'modularity': 'Modularity',
                                        'asyn_lpa': 'Asynchronous Label Propagation',
                                        'label_propagation': 'Label Propagation'}
                        }
                    }
                },
                'within_inter_cluster': {
                    'name': 'Within- and Interclustering',
                    'parameter': {
                        'community_detection_method': {
                            'description': 'Community detection method',
                            'options': {'modularity': 'Modularity',
                                        'asyn_lpa': 'Asynchronous Label Propagation',
                                        'label_propagation': 'Label Propagation'}
                        }
                    }
                }
            }
            }
    return info


class LinkPredictor:
    """
    class for performing link prediction
    """

    def __init__(self, algorithm):
        """
        init a community detector using the given `algorithm`
        :param algorithm:
        """
        self.algorithm = algorithm
        self.methods = {
            'resource_allocation_index': resource_allocation_index,
            'resource_allocation': resource_allocation_index,
            'jaccard_coefficient': jaccard_coefficient,
            'jaccard': jaccard_coefficient,
            'adamic_adar_index': adamic_adar_index,
            'adamic_adar': adamic_adar_index,
            'preferential_attachment': preferential_attachment,
            'count_number_soundarajan_hopcroft': count_number_soundarajan_hopcroft,
            'resource_allocation_index_soundarajan_hopcroft': resource_allocation_index_soundarajan_hopcroft,
            'within_inter_cluster': within_inter_cluster
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
