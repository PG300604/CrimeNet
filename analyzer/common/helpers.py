import networkx as nx
from scipy.sparse import csr_matrix

def is_valid(edge, params):
    """
    to check if the input edge satisfies the conditions in params
    :param edge: dictionary contain information about an edge, in following format
                    {
                        "source": id of source node,
                        "target": id of target node,
                        "observed": True if the edge is observed in data, False otherwise (e.g., the edge is
                            inferred by latent link detection algorithms)
                        "properties": dictionary that contains properties of the edge, in the following format
                                    {
                                        "weight": optional, weight of the edge
                                        "type": type of the edge, e.g., "work for", or "friend of",
                                        "confidence": optional, confidence/certainty of the edge
                                        ...
                                    }
                        ...
                    }
    :param params: options for filtering edges
    :return:
    """
    # TODO: implement the condition checker
    return True


def get_edges_and_node_ids(network, params):
    nodes = {}
    edges = []
    node_ids = []

    network_edges = network.get('edges')

    for e in network_edges:
        if is_valid(e, params):
            source = e['source']
            target = e['target']
            if source not in nodes:
                source_index = len(node_ids)
                nodes[source] = source_index
                node_ids.append(source)
            else:
                source_index = nodes[source]

            if target not in nodes:
                target_index = len(node_ids)
                nodes[target] = target_index
                node_ids.append(target)
            else:
                target_index = nodes[target]

            edges.append((source_index, target_index))

    return edges, node_ids


def convert_to_nx_undirected_graph(network, params=None, node_is_str=False, **kwargs):
    """
    convert a undirected network in edge list format into `networkx` network
    """
    edges, node_ids = get_edges_and_node_ids(network, params)

    graph = nx.Graph()
    if node_is_str:
        graph.add_edges_from([(str(u), str(v)) for u, v in edges])
    else:
        graph.add_edges_from(edges)
    return graph, node_ids


def convert_to_nx_directed_graph(network, params=None, node_is_str=False, **kwargs):
    """
    convert a directed network in edge list format into `networkx` network
    """
    edges, node_ids = get_edges_and_node_ids(network, params)

    graph = nx.DiGraph()
    if node_is_str:
        graph.add_edges_from([(str(u), str(v)) for u, v in edges])
    else:
        graph.add_edges_from(edges)
    return graph, node_ids

def convert_to_csr_sparse_matrix(network, params=None):
    """
    convert a network in edge list format into scipy  csr_sparse matrix
    :param network: is a dictionany having two keys 'edges' and 'nodes', 
                        value of key 'edges' is list of dictionaries, each contains selected information about an edge, 
                        each in the following format
                            {
                                "source": id of source node,
                                "target": id of target node,
                                "observed": True if the edge is observed in data, False otherwise (e.g., the edge is
                                    inferred by latent link detection algorithms)
                                "properties": dictionary that contains properties of the edge, in the following format
                                            {
                                                "weight": optional, weight of the edge
                                                "type": type of the edge, e.g., "work for", or "friend of",
                                                "confidence": optional, confidence/certainty of the edge
                                                ...
                                            }
                                ...
                            }
    :param params: options for filtering edges #TODO: to add options
    :return: (nx_network, node_ids)
        matrix: scipy csr_sparse matrix
        node_ids: ids of nodes in input matrix, i.e., node_ids[i] is original id node i of nx_network
    """
    nodes = {}
    node_ids = []
    rows = []
    cols = []
    weights = []

    network_edges = network.get('edges')

    for e in network_edges:
        if is_valid(e, params):
            source = e['source']
            target = e['target']
            if 'weight' in e['properties']:
                weight = e['properties']['weight']
            else:
                weight = 1.0
            if source not in nodes:
                source_index = len(node_ids)
                nodes[source] = source_index
                node_ids.append(source)
            else:
                source_index = nodes[source]

            if target not in nodes:
                target_index = len(node_ids)
                nodes[target] = target_index
                node_ids.append(target)
            else:
                target_index = nodes[target]
            rows.append(source_index)
            cols.append(target_index)
            weights.append(weight)
            # Add symmetric edge for undirected representation
            rows.append(target_index)
            cols.append(source_index)
            weights.append(weight)

    n_nodes = len(node_ids)
    matrix = csr_matrix((weights, (rows, cols)), shape=(n_nodes, n_nodes))
    matrix = matrix.asfptype()
    return matrix, node_ids
