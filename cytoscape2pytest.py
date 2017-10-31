# !/usr/bin/python3
"""
cytoscape2pytest - Automating the creation of cytoscape graphs from network tables produced by GOcats runscripts
"""

import os
from py2cytoscape.data.cynetwork import CyNetwork
from py2cytoscape.data.cyrest_client import CyRestClient
from py2cytoscape.data.style import StyleUtil
import py2cytoscape.util.cytoscapejs as cyjs
import py2cytoscape.cytoscapejs as renderer

import networkx as nx
import pandas as pd
import json

cy = CyRestClient(ip='0.0.0.0', port=8888)
cy.session.delete()

table_data = pd.read_csv('NetworkTable.csv', names=['source', 'target'], index_col=None)
table_data['interaction'] = 1  # Column needed for the create_from_dataframe function, these are nonsense values that won't be used.

concept_subgraphs = cy.network.create_from_dataframe(
										table_data, source_col='source', target_col='target', 
										interaction_col='interaction', name='GOcats concept subgraphs'
										)

cy.layout.apply(name='kamada-kawai', network=concept_subgraphs)
