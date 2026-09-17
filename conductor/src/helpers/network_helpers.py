"""
Helpers to transform the network
"""
def network_to_split(network, is_parse_wp5=False):
    """
    Split network on nodes and edges

    :param network: list of nodes and edges or wp5 network
    :param is_parse_wp5: Should wp5 network be parsed
    :returns: dictionary with 'nodes' and 'edges' lists
    """
    edges = []
    nodes = []
    for i in network:
        if i["type"] == "edge":
            edges.append(i)
        else:
            nodes.append(i)
        del i["type"]
    return {
        "edges": edges,
        "nodes": nodes
    }


def split_to_network(nodes, edges):
    """
    Merge nodes and edges into single list

    :param nodes: nodes of the network
    :param edges: edges of the network
    :returns: list of all network elements combined
    """
    for n in nodes:
        n["type"] = "node"
    for e in edges:
        e["type"] = "edge"
    return nodes + edges
