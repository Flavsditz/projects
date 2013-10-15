#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      flavio
#
# Created:     20.01.2013
# Copyright:   (c) flavio 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#!/usr/bin/env python
"""
Draw a graph with matplotlib, color edges.
You must have matplotlib>=87.7 for this to work.
"""
__author__ = """Aric Hagberg (hagberg@lanl.gov)"""
try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx

G=nx.star_graph(20)
pos=nx.spring_layout(G)
colors=range(20)
nodesize = 20 * [100]
labels=range(20)

nx.draw_networkx_nodes(G,pos,node_size=20 * [600], node_color='#00ff00')
nx.draw_networkx_nodes(G,pos,node_size=20 * [300], node_color='#ff0000')
nx.draw_networkx_edges(G,pos,edge_color="#0000ff",width=8)
nx.draw_networkx_edges(G,pos,edge_color="#00ff00",width=5)
nx.draw_networkx_edges(G,pos,edge_color="#ff0000",width=2)
nx.draw_networkx_labels(G,pos)
plt.savefig("edge_colormap.png") # save as png
plt.show() # display