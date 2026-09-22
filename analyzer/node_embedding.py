import sys
import os
import networkx as nx
from scipy.sparse.linalg import svds
from sklearn.decomposition import NMF

# find path to root directory of the project so as to import from other packages
path2root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path2root not in sys.path:
    sys.path.append(path2root)

import analyzer.common.helpers as helpers
from analyzer.ge.models.deepwalk import DeepWalk
from analyzer.ge.models.node2vec import Node2Vec
from analyzer.ge.models.line import LINE


def svd(network, params):
    """
    perform node embedding by singular value decomposition
    :param network:
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'vectors': a dictionary of vector of nodes in network, each vector is a numpy array
        }
    """
    try:
        matrix, node_ids = helpers.convert_to_csr_sparse_matrix(network, params)
        k = params['K']
        print('shape =', matrix.shape)
        print(matrix)
        u, _, _ = svds(matrix, k)
        vectors = [(node_ids[i], u[i]) for i in range(len(node_ids))]
        result = {'success': 1, 'message': 'the task is performed successfully', 'vectors': dict(vectors)}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'vectors': None}
        return result


def nmf(network, params):
    """
    perform node embedding by non-negative matrix factorization
    :param network:
    :param params:
     :return: dictionary, in the form
    {
        'success': 1 if success, 0 otherwise
        'message': a string
        'vectors': a dictionary of vector of nodes in network, each vector is a numpy array
    }
    """
    try:
        matrix, node_ids = helpers.convert_to_csr_sparse_matrix(network, params)
        k = params['K']
        model = NMF(n_components=k)
        w = model.fit_transform(matrix)
        vectors = [(node_ids[i], w[i]) for i in range(len(node_ids))]
        result = {'success': 1, 'message': 'the task is performed successfully', 'vectors': dict(vectors)}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'vectors': None}
        return result


def node2vec(network, params):
    """
    perform node embedding by node2vec
    :param network:
    :param params:
     :return: dictionary, in the form
    {
        'success': 1 if success, 0 otherwise
        'message': a string
        'vectors': a dictionary of vector of nodes in network, each vector is a numpy array
    }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_directed_graph(network, params, node_is_str=True)
        k = params['K']
        # Graph summary
        print(f"Graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")

        model = Node2Vec(graph, walk_length=40, num_walks=80,
                         p=0.25, q=4, workers=8, use_rejection_sampling=0)
        model.train(embed_size=k, window_size=5, workers=8, iter=10)
        embeddings = model.get_embeddings()

        vectors = [(node_ids[i], embeddings.get(str(i))) for i in range(len(node_ids))]
        result = {'success': 1, 'message': 'the task is performed successfully', 'vectors': dict(vectors)}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'vectors': None}
        return result


def deepwalk(network, params):
    """
    perform node embedding by DeepWalk
    :param network:
    :param params:
     :return: dictionary, in the form
    {
        'success': 1 if success, 0 otherwise
        'message': a string
        'vectors': a dictionary of vector of nodes in network, each vector is a numpy array
    }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_directed_graph(network, params, node_is_str=True)
        k = params['K']
        # Graph summary
        print(f"Graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")

        model = DeepWalk(graph, walk_length=40, num_walks=80, workers=8)
        model.train(embed_size=k, window_size=5, workers=8, iter=10)
        embeddings = model.get_embeddings()

        vectors = [(node_ids[i], embeddings.get(str(i))) for i in range(len(node_ids))]
        result = {'success': 1, 'message': 'the task is performed successfully', 'vectors': dict(vectors)}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'vectors': None}
        return result


def line(network, params):
    """
    perform node embedding by Large-scale Information Network Embedding (LINE)
    :param network:
    :param params:
     :return: dictionary, in the form
    {
        'success': 1 if success, 0 otherwise
        'message': a string
        'vectors': a dictionary of vector of nodes in network, each vector is a numpy array
    }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_directed_graph(network, params, node_is_str=True)
        k = params['K']
        # Graph summary
        print(f"Graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")

        model = LINE(graph, embedding_size=k, order='second')
        model.train(batch_size=1024, epochs=100, verbose=2)
        embeddings = model.get_embeddings()

        vectors = [(node_ids[i], embeddings.get(str(i))) for i in range(len(node_ids))]
        result = {'success': 1, 'message': 'the task is performed successfully', 'vectors': dict(vectors)}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network', 'vectors': None}
        return result


def sine(network, params):
    pass


def role2vec(network, params):
    pass


def metapath2vec(network, params):
    pass


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
    info = {'name': 'Node Embedding',
            'methods': {
                'svd': {
                    'name': 'Singular Value Decomposition',
                    'parameter': {
                        'K': {
                            'description': 'The embedding dimension',
                            'options': {'Integer': 'Integer'}
                        }
                    }
                },
                'nmf': {
                    'name': 'Non-negative Matrix Factorization',
                    'parameter': {
                        'K': {
                            'description': 'The embedding dimension',
                            'options': {'Integer': 'Integer'}
                        }
                    }
                }
            }
            }

    # 'deepwalk': {'K: the embedding dimension'},
    # 'line': {'K: the embedding dimension'},
    # 'node2vec': {'K: the embedding dimension'},
    # 'sine': {'K: the embedding dimension'},
    # 'role2vec': {'K: the embedding dimension'},
    # 'metapath2vec': {'K: the embedding dimension'}

    return info


class NodeEmbedder:
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
            'svd': svd,
            'nmf': nmf,
            'deepwalk': deepwalk,
            'node2vec': node2vec,
            'line': line,
            'sine': sine,
            'role2vec': role2vec,
            'metapath2vec': metapath2vec
            # TODO: to add more methods for attributed networks and knowledge networks
        }

    def perform(self, network, params):
        """
        performing
        :param network:
        :param params:
        :return:
        """
        return self.methods[self.algorithm](network, params)
