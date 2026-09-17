import pytest
from conductor.src.helpers.network_helpers import network_to_split, split_to_network


def test_network_to_split_should_return_nodes_and_edges_dictionaries():
    """ network_to_split should return dictionary with nodes and edges keys """
    example_network = [
        {"type": "node", "id": "Satam_Suqami", "properties": {"type": "person", "name": "Satam Suqami", "flight": "AA #11 WTC North", "attend_Las_Vegas_Meeting": False}},
        {"type": "node", "id": "Wail_Alshehri", "properties": {"type": "person", "name": "Wail Alshehri", "flight": "AA #11 WTC North", "attend_Las_Vegas_Meeting": False}},
        {"type": "edge", "source": "Majed_Moqed", "target": "Khalid_Al-Mihdhar", "properties": {"type": "prior_contact", "observed": True, "weight": 1}},
        {"type": "edge", "source": "Majed_Moqed", "target": "Nawaf_Alhazmi", "properties": {"type": "prior_contact", "observed": True, "weight": 1}}
    ]
    result = network_to_split(example_network)
    assert example_network[0] in result["nodes"] and example_network[1] in result["nodes"]
    assert example_network[2] in result["edges"] and example_network[3] in result["edges"]

def test_split_to_network_should_return_list_of_nodes_and_edges_combined():
    """ split_to_network should combine edges and nodes """
    example_split = {
        "edges": [
            {"source": "Majed_Moqed", "target": "Khalid_Al-Mihdhar", "properties": {"type": "prior_contact", "observed": True, "weight": 1}},
            {"source": "Majed_Moqed", "target": "Nawaf_Alhazmi", "properties": {"type": "prior_contact", "observed": True, "weight": 1}}
        ],
        "nodes": [
            {"id": "Satam_Suqami", "properties": {"type": "person", "name": "Satam Suqami", "flight": "AA #11 WTC North", "attend_Las_Vegas_Meeting": False}},
            {"id": "Wail_Alshehri", "properties": {"type": "person", "name": "Wail Alshehri", "flight": "AA #11 WTC North", "attend_Las_Vegas_Meeting": False}}
        ]
    }
    result = split_to_network(example_split["nodes"], example_split["edges"])
    assert all(el in result for el in example_split["edges"] + example_split["nodes"])
