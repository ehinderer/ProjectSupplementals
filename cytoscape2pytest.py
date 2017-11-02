# !/usr/bin/python3
"""
cytoscape2pytest - Automating the creation of cytoscape graphs from network tables produced by GOcats runscripts
"""

from py2cytoscape.data.cynetwork import CyNetwork
from py2cytoscape.data.cyrest_client import CyRestClient
import os
import pandas as pd
import json
import jsonpickle


def jsonpickle_load(filename):
    """Takes a JsonPickle file and loads in the JsonPickle object into a Python object.

    :param file_handle filename: A path to a JsonPickle file.
    """
    f = open(filename)
    json_str = f.read()
    obj = jsonpickle.decode(json_str, keys=True)  # Use_jsonpickle=True used to prevent jsonPickle from encoding dictkeys to strings.
    return obj

# Translation from GO id to english name
id_translation_dict = jsonpickle_load('id_translation.json_pickle')

# Start the Cytoscape session
cy = CyRestClient(ip='0.0.0.0', port=1234)
cy.session.delete()

# Format the graph data from GOcats
table_data = pd.read_csv('NetworkTable.csv', names=['source', 'target'], index_col=None)
table_data['interaction'] = 1  # Column needed for the create_from_dataframe function, these are nonsense values that won't be used.

# Make a set of the concept-representative GO terms
target_ids = set([go_id for go_id in table_data['target']])

# Create a Cytoscape network from the data table
concept_subgraphs = cy.network.create_from_dataframe(table_data, source_col='source', target_col='target', interaction_col='interaction', name='GOcats concept subgraphs')

# Get the data table back form the network, and create a mapping of network node suids to GO terms
node_table = concept_subgraphs.get_node_table()
suid_index = dict(zip(node_table['shared name'], node_table.index))

# Get the network view for editing
view_id_list = concept_subgraphs.get_views()
view = concept_subgraphs.get_view(view_id_list[0], format='view')

# Edit the poperties of category-representative nodes
for go_id in target_ids:
    view.update_node_views(visual_property='NODE_FILL_COLOR', values={suid_index[go_id]:'#5697ff'})
    view.update_node_views(visual_property='NODE_HEIGHT', values={suid_index[go_id]:200})
    view.update_node_views(visual_property='NODE_WIDTH', values={suid_index[go_id]:200})
    view.update_node_views(visual_property='NODE_LABEL', values={suid_index[go_id]:id_translation_dict[go_id]})
    view.update_node_views(visual_property='NODE_LABEL_COLOR', values={suid_index[go_id]:'#ffffff'})
    view.update_node_views(visual_property='NODE_LABEL_FONT_SIZE', values={suid_index[go_id]:50})

# Apply layout to organize graph 
cy.layout.apply(name='kamada-kawai', network=concept_subgraphs)
