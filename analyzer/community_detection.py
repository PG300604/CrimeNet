import sys
import os
import itertools
import warnings
from scipy.cluster.hierarchy import ClusterWarning
import numpy as np
import networkx.algorithms.community as methods
import networkx
from sklearn.cluster import SpectralClustering
from sklearn.cluster import AgglomerativeClustering

# find path to root directory of the project so as to import from other packages
path2root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path2root not in sys.path:
    sys.path.append(path2root)

import analyzer.common.helpers as helpers


def _generate_communities_and_membership(nx_communities, node_ids):
    communities = []
    membership = {}
    for c in range(len(nx_communities)):
        for u in nx_communities[c]:
            nid = node_ids[u]
            if nid in membership:
                membership[nid][c] = 1.0
            else:
                membership[nid] = {c: 1.0}
        communities.append(dict([(node_ids[u], 1.0) for u in nx_communities[c]]))
    return communities, membership


def k_clique_communities(network, params):
    """
    wrapper for NetworkX's k_clique_communities algorithm
    :param network:
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'communities': communities - list of communities found, each is a dictionary of member nodes' id, and their membership
            'membership': membership - dictionary, membership[u] is a dictionary of communities of u and its membership in those communities
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        if graph.number_of_nodes() < 2 or graph.number_of_edges() == 0:
            return {'success': 0, 'message': 'Community detection requires at least 2 connected nodes.', 'communities': None, 'membership': None}
        # If no parameter were given, use 3 as default.
        # May not be the most elegant solution but is the easiest for now.
        try:
            k = params['K']
        except KeyError:
            k = 3
        nx_comms = list(methods.k_clique_communities(graph, k))
        communities, membership = _generate_communities_and_membership(nx_comms, node_ids)
        result = {'success': 1, 'message': 'the task is performed successfully', 'communities': communities,
                  'membership': membership}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network',
                  'communities': None,
                  'membership': None}
        return result


def greedy_modularity_communities(network, params):
    """
    wrapper for NetworkX's greedy_modularity_communities algorithm
    :param network:
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'communities': communities - list of communities found, each is a dictionary of member nodes' id, and their membership
            'membership': membership - dictionary, membership[u] is a dictionary of communities of u and its membership in those communities
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        if graph.number_of_nodes() < 2 or graph.number_of_edges() == 0:
            return {'success': 0, 'message': 'Community detection requires at least 2 connected nodes.', 'communities': None, 'membership': None}
        nx_comms = list(methods.greedy_modularity_communities(graph))
        communities, membership = _generate_communities_and_membership(nx_comms, node_ids)
        result = {'success': 1, 'message': 'the task is performed successfully', 'communities': communities,
                  'membership': membership}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network',
                  'communities': None,
                  'membership': None}
        return result


def asyn_lpa_communities(network, params):
    """
    wrapper for NetworkX's asynchronous label propagation algorithm
    :param network:
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'communities': communities - list of communities found, each is a dictionary of member nodes' id, and their membership
            'membership': membership - dictionary, membership[u] is a dictionary of communities of u and its membership in those communities
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_directed_graph(network)
        if graph.number_of_nodes() < 2 or graph.number_of_edges() == 0:
            return {'success': 0, 'message': 'Community detection requires at least 2 connected nodes.', 'communities': None, 'membership': None}
        nx_comms = list(methods.asyn_lpa_communities(graph))
        communities, membership = _generate_communities_and_membership(nx_comms, node_ids)
        result = {'success': 1, 'message': 'the task is performed successfully', 'communities': communities,
                  'membership': membership}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network',
                  'communities': None,
                  'membership': None}
        return result


def label_propagation_communities(network, params):
    """
    wrapper for NetworkX's semi-synchronous label propagation algorithm
    :param network:
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'communities': communities - list of communities found, each is a dictionary of member nodes' id, and their membership
            'membership': membership - dictionary, membership[u] is a dictionary of communities of u and its membership in those communities
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        if graph.number_of_nodes() < 2 or graph.number_of_edges() == 0:
            return {'success': 0, 'message': 'Community detection requires at least 2 connected nodes.', 'communities': None, 'membership': None}
        nx_comms = list(methods.label_propagation_communities(graph))
        communities, membership = _generate_communities_and_membership(nx_comms, node_ids)
        result = {'success': 1, 'message': 'the task is performed successfully', 'communities': communities,
                  'membership': membership}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network',
                  'communities': None,
                  'membership': None}
        return result


def kernighan_lin_bipartition(network, params):
    """
    wrapper for NetworkX's Kernighan–Lin bipartition algorithm to partition a graph into two blocks
    :param network:
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'communities': communities - list of communities found, each is a dictionary of member nodes' id, and their membership
            'membership': membership - dictionary, membership[u] is a dictionary of communities of u and its membership in those communities
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        nx_comms = list(methods.kernighan_lin_bisection(graph))
        communities, membership = _generate_communities_and_membership(nx_comms, node_ids)
        result = {'success': 1, 'message': 'the task is performed successfully', 'communities': communities,
                  'membership': membership}
        return result
    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network',
                  'communities': None,
                  'membership': None}
        return result


def spectral_communities(network, params):
    """
    wrapper for NetworkX's k_clique_communities algorithm
    :param network:
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise
            'message': a string
            'communities': communities - list of communities found, each is a dictionary of member nodes' id, and their membership
            'membership': membership - dictionary, membership[u] is a dictionary of communities of u and its membership in those communities
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        if graph.number_of_nodes() < 2 or graph.number_of_edges() == 0:
            return {'success': 0, 'message': 'Community detection requires at least 2 connected nodes.', 'communities': None, 'membership': None}
        # If no parameter were given, use 3 as default.
        # May not be the most elegant solution but is the easiest for now.
        try:
            k = params['K']
        except KeyError:
            k = 3

        adj_matrix = networkx.adjacency_matrix(graph)
        clustering = SpectralClustering(n_clusters=k, assign_labels="discretize", random_state=0).fit(adj_matrix)
        # print(clustering.labels_)
        communities = [{}] * k
        membership = {}
        for u in range(len(clustering.labels_)):
            c = clustering.labels_[u]
            nid = node_ids[u]
            if nid in membership:
                membership[nid][c] = 1.0
            else:
                membership[nid] = {c: 1.0}
            communities[c][nid] = 1.0

        result = {'success': 1, 'message': 'the task is performed successfully', 'communities': communities,
                  'membership': membership}
        return result

    except Exception as e:
        print(e)
        result = {'success': 0, 'message': 'this algorithm is not suitable for the input network',
                  'communities': None,
                  'membership': None}
        return result


def louvain_communities_method(network, params):
    """
    wrapper for NetworkX's louvain_communities algorithm
    :param network:
    :param params:
    :return: dictionary, in the form
        {
            'success': 1 if success, 0 otherwise,
            'message': a string,
            'algorithm': 'louvain',
            'communities': communities,
            'membership': membership,
            'num_communities': int,
            'nodes_analyzed': int
        }
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        if 'nodes' in network and network['nodes']:
            for n in network['nodes']:
                n_id = n.get('id', n.get('name', '')) if isinstance(n, dict) else str(n)
                if n_id and n_id not in node_ids:
                    graph.add_node(len(node_ids))
                    node_ids.append(n_id)

        if graph.number_of_nodes() < 2 or graph.number_of_edges() == 0:
            return {
                'success': 0,
                'message': 'Community detection requires at least 2 connected nodes.',
                'algorithm': 'louvain',
                'communities': None,
                'membership': None,
                'num_communities': 0,
                'nodes_analyzed': len(node_ids)
            }

        resolution = 1.0
        if params and 'resolution' in params:
            try:
                resolution = float(params['resolution'])
            except (ValueError, TypeError):
                resolution = 1.0

        seed = 42
        nx_comms = list(methods.louvain_communities(graph, resolution=resolution, seed=seed))
        nx_comms.sort(key=lambda s: len(s), reverse=True)
        communities, membership = _generate_communities_and_membership(nx_comms, node_ids)
        result = {
            'success': 1,
            'message': 'the task is performed successfully',
            'algorithm': 'louvain',
            'communities': communities,
            'membership': membership,
            'num_communities': len(nx_comms),
            'nodes_analyzed': len(node_ids)
        }
        return result
    except Exception as e:
        print(e)
        result = {
            'success': 0,
            'message': 'this algorithm is not suitable for the input network: ' + str(e),
            'algorithm': 'louvain',
            'communities': None,
            'membership': None,
            'num_communities': 0,
            'nodes_analyzed': 0
        }
        return result


def hierarchical_communities(network, params):
    """
    Hierarchical clustering community detection algorithm and tree structure generator.
    Computes flat community assignments for Cytoscape node coloring and a hierarchical
    tree structure (root -> major clusters -> subclusters -> leaf entities).
    """
    try:
        graph, node_ids = helpers.convert_to_nx_undirected_graph(network)
        if 'nodes' in network and network['nodes']:
            for n in network['nodes']:
                n_id = n.get('id', n.get('name', '')) if isinstance(n, dict) else str(n)
                if n_id and n_id not in node_ids:
                    graph.add_node(len(node_ids))
                    node_ids.append(n_id)

        n_nodes = len(node_ids)
        if n_nodes < 2 or graph.number_of_edges() == 0:
            return {
                'success': 0,
                'message': 'Community detection requires at least 2 connected nodes.',
                'algorithm': 'hierarchical',
                'communities': [],
                'membership': {},
                'tree': None,
                'stats': {'total_entities': n_nodes, 'total_clusters': 0, 'hierarchy_depth': 0},
                'num_communities': 0,
                'nodes_analyzed': n_nodes
            }

        try:
            k = int(params['K'])
        except (KeyError, TypeError, ValueError):
            k = 4
        k = max(1, min(k, n_nodes))

        # Adjacency matrix as float array
        adj_matrix = networkx.adjacency_matrix(graph).toarray().astype(float)

        # Flat clustering for graph node coloring
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', ClusterWarning)
            if n_nodes > 1 and k > 1:
                try:
                    clustering = AgglomerativeClustering(n_clusters=k).fit(adj_matrix)
                    labels = clustering.labels_
                except Exception:
                    labels = np.array([i % k for i in range(n_nodes)])
            else:
                labels = np.zeros(n_nodes, dtype=int)

        communities = [{} for _ in range(k)]
        membership = {}
        for u in range(n_nodes):
            c = int(labels[u])
            nid = node_ids[u]
            membership[nid] = {c: 1.0}
            communities[c][nid] = 1.0

        # Build hierarchical tree
        cluster_counter = [0]
        max_tree_depth = [0]

        node_metadata = network.get('node_metadata', {})

        def build_subtree(indices, depth, max_depth, branch_factor, prefix):
            if depth > max_tree_depth[0]:
                max_tree_depth[0] = depth

            # Base case: small group or reached max depth -> return leaf entity nodes
            if len(indices) <= 3 or depth >= max_depth:
                children = []
                for idx in indices:
                    nid = str(node_ids[idx])
                    meta = node_metadata.get(nid, {})
                    label = meta.get('label') or meta.get('name') or nid
                    ntype = meta.get('type') or 'person'
                    children.append({
                        'id': nid,
                        'label': str(label),
                        'type': str(ntype),
                        'is_leaf': True,
                        'size': 1,
                        'nodes': [nid]
                    })
                return children

            sub_adj = adj_matrix[np.ix_(indices, indices)]
            sub_k = min(branch_factor, len(indices))
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', ClusterWarning)
                    sub_model = AgglomerativeClustering(n_clusters=sub_k).fit(sub_adj)
                    sub_labels = sub_model.labels_
            except Exception:
                sub_labels = [i % sub_k for i in range(len(indices))]

            children = []
            for sc in range(sub_k):
                sub_idx = [indices[i] for i in range(len(indices)) if sub_labels[i] == sc]
                if not sub_idx:
                    continue
                cluster_counter[0] += 1
                c_id = f'{prefix}-{sc+1}'
                c_label = f'Group {chr(65 + sc)}' if depth == 2 else f'Sub-cluster {sc+1}'
                all_sub_nids = [str(node_ids[i]) for i in sub_idx]
                sub_children = build_subtree(sub_idx, depth + 1, max_depth, branch_factor, c_id)
                children.append({
                    'id': c_id,
                    'label': f'{c_label} ({len(sub_idx)} entities)',
                    'is_leaf': False,
                    'size': len(sub_idx),
                    'nodes': all_sub_nids,
                    'children': sub_children
                })
            return children

        major_clusters = []
        for c in range(k):
            sub_idx = [i for i in range(n_nodes) if labels[i] == c]
            if not sub_idx:
                continue
            cluster_counter[0] += 1
            c_id = f'cluster-{c+1}'
            c_label = f'Cluster {c+1}'
            all_sub_nids = [str(node_ids[i]) for i in sub_idx]
            sub_children = build_subtree(sub_idx, depth=2, max_depth=4, branch_factor=2, prefix=c_id)
            major_clusters.append({
                'id': c_id,
                'label': f'{c_label} ({len(sub_idx)} entities)',
                'is_leaf': False,
                'size': len(sub_idx),
                'nodes': all_sub_nids,
                'children': sub_children
            })

        tree = {
            'id': 'root',
            'label': f'Full Network ({n_nodes} entities)',
            'is_leaf': False,
            'size': n_nodes,
            'nodes': [str(nid) for nid in node_ids],
            'children': major_clusters
        }

        stats = {
            'total_entities': n_nodes,
            'total_clusters': cluster_counter[0],
            'hierarchy_depth': max_tree_depth[0] + 1
        }

        result = {
            'success': 1,
            'message': 'the task is performed successfully',
            'algorithm': 'hierarchical',
            'communities': communities,
            'membership': membership,
            'tree': tree,
            'stats': stats,
            'num_communities': len(communities),
            'nodes_analyzed': n_nodes
        }
        return result
    except Exception as e:
        print(e)
        result = {
            'success': 0,
            'message': 'this algorithm is not suitable for the input network: ' + str(e),
            'algorithm': 'hierarchical',
            'communities': None,
            'membership': None,
            'tree': None,
            'stats': None,
            'num_communities': 0,
            'nodes_analyzed': 0
        }
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
    info = {'name': 'Community Detection',
            'methods': {
                'louvain': {
                    'name': 'Louvain',
                    'parameter': {}
                },
                'modularity': {
                    'name': 'Modularity Maximization',
                    'parameter': {}
                },
                'label_propagation': {
                    'name': 'Label Propagation',
                    'parameter': {}
                },
                'hierarchical': {
                    'name': 'Hierarchical clustering',
                    'parameter': {
                        'K': {
                            'description': 'number of communities',
                            'options': {'Integer': [2, 3, 4, 5, 6, 7]}
                        }
                    }
                },
                'k_cliques': {
                    'name': 'K-clique',
                    'parameter': {
                        'K': {
                            'description': 'Size of smallest clique.',
                            'options': {'Integer': [3, 4, 5, 6, 7]}
                        }
                    }
                },
                'asyn_lpa': {
                    'name': 'Asynchronous Label Propagation',
                    'parameter': {}
                },
                'bipartition': {
                    'name': 'Kernighan–Lin Bipartition',
                    'parameter': {}
                },
                'spectral': {
                    'name': 'Spectral clustering',
                    'parameter': {
                        'K': {
                            'description': 'number of communities',
                            'options': {'Integer': [3, 4, 5, 6, 7]}
                        }
                    }
                }
            }
            }
    return info


class CommunityDetector:
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
            'louvain': louvain_communities_method,
            'k_cliques': k_clique_communities,
            'modularity': greedy_modularity_communities,
            'asyn_lpa': asyn_lpa_communities,
            'label_propagation': label_propagation_communities,
            'bipartition': kernighan_lin_bipartition,
            'spectral': spectral_communities,
            'hierarchical': hierarchical_communities
        }

    def perform(self, network, params):
        """
        performing
        :param network:
        :param params:
        :return:
        """
        return self.methods[self.algorithm](network, params)
