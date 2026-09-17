from copy import deepcopy
import sys, scipy.special, json, re
import numpy as np


def is_valid_node(node_properties, params):
    """
    check if a node with node_properties satisfy the selection criteria
    :param node_properties: dictionary containing information about the node
    :param params: dictionary containing information about the selection criteria
    :return:
    """
    # TODO: to be refactored
    if params is None:
        return True
    else:
        for p in params:
            if p not in node_properties:
                return False
            value = params[p]
            if node_properties[p] != value:
                return False
        return True


def is_valid_edge(edge_properties, params):
    """
    check if a node with node_properties satisfy the selection criteria
    :param edge_properties: dictionary containing information about the node
    :param params: dictionary containing information about the selection criteria
    :return:
    """
    # TODO: to be refactored
    if params is None:
        return True
    else:
        for p in params:
            if p not in edge_properties:
                return False
            value = params[p]
            if edge_properties[p] != value:
                return False
        return True


def min_max_scaling(value, min_value, max_value, value_range=(0, 1)):
    """
    Normalize a value using min-max feature scaling in a given range.
    :param value: A number to map to the given range.
    :param min_value: Minimum of numbers in domain.
    :param max_value: Maximum of numbers in domain.
    :param value_range: Tuple defining the new range of values.
    :return:
    """
    return value_range[0] + (((value - min_value) * (value_range[1] - value_range[0])) / (max_value - min_value))


def compare_edge_type(properties1, properties2):
    print('properties1 = ', properties1)
    print('properties2 = ', properties2)
    if properties1 is None:
        properties1 = dict()
    if properties2 is None:
        properties2 = dict()
    if 'type' not in properties1:
        if 'type' not in properties2:
            return True
        else:
            return False
    else:
        if 'type' not in properties2:
            return False
        else:
            if properties1['type'] == properties2['type']:
                return True
            return False


def old_network_to_new_network(nodes, edges):
    """
    Translate old network object format to new
    :param nodes: List of network nodes
    :param edges: List of network edges
    :returns: dict with new nodes and links
    """
    updated_nodes = deepcopy(nodes)
    updated_edges = deepcopy(edges)
    for n in updated_nodes:
        for p in n["properties"]:
            n[p] = n["properties"][p]
        del n["properties"]
    for e in updated_edges:
        for p in e["properties"]:
            e[p] = e["properties"][p]
        del e["properties"]
    return {
        "nodes": updated_nodes,
        "links": updated_edges
    }
