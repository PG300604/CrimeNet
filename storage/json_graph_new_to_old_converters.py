import os
import sys
import json

import networkx as nx
import numpy as np

from networkx.readwrite import json_graph

tokens = os.path.abspath(__file__).split('/')
path2root = '/'.join(tokens[:-2])
if path2root not in sys.path:
    sys.path.append(path2root)

print('converters: path2root = ', path2root)

if path2root not in sys.path:
    sys.path.append(path2root)

from storage import helpers

fp_input = 'datasets/preprocessed/israel_lea_inp_burglary_offender_id_network.json'
fn = fp_input.replace('.json', '')

with open(fp_input) as json_file:
    json_data = json.load(json_file)

input_graph = json_graph.node_link_graph(json_data)
print(nx.info(input_graph))


fp_output = fn + '_old_format.json'
fp = open(fp_output, 'w')

for node_id, node_data in input_graph.nodes(data=True):
    node = {
        'type': 'node',
        'id': node_id,
        'properties': node_data
    }
    node = json.dumps(node)
    fp.write('%s\n' % node)

for source_id, target_id, edge_data in input_graph.edges(data=True):
    edge = {
        'type': 'edge',
        'source': source_id,
        'target': target_id,
        'properties': edge_data
    }
    edge = json.dumps(edge)
    fp.write('%s\n' % edge)

fp.close()
