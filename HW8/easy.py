import requests
import json
import time
from datetime import datetime, timedelta
from itertools import permutations


import os

# Run this install commands the first time, then comment out these lines (or delete them)
# Note: these commands could also be run in a terminal.  Running them here, so the entire program below works
#os.system("sudo pip3 install networkx")
#os.system("sudo apt-get install python3-matplotlib")

import matplotlib
matplotlib.use('Agg') # putting matplolib into server-only mode, no GUI

import matplotlib.pyplot as plt

import networkx as nx
from networkx.classes.function import path_weight

curr_dir = os.path.dirname(__file__) # get the current directory of this file

edges_fil = curr_dir + "/" + "edges.txt" # dirname and __file__ (this file) returns the current folder
graph_visual_fil = curr_dir + "/" + "graph_visual.png"

file = open(edges_fil) 

g = nx.DiGraph() # created directed graph



############################################################
# STEP 1 - Create Graph
# get all edges from the txt file
edges = []

for line in file.readlines():
    node1, node2, weight = line.split(",")
    weight = int(weight)
    edges.append((node1, node2, weight)) # add edge to a list of tuples
    
print(edges)
g.add_weighted_edges_from(edges) 

# example of adding the edges to a graph one at a time
# code above adds all the edges to the graph at once
# for e in edges:
#     g.add_edge(e[0], e[1], weight=e[2])

# print all nodes
print(g.nodes)


#heres the actual funtction to return number of nodes
def countNodes(graph):
    i=0
    for node in graph.nodes:
        i+=1
    print(i)

countNodes(g)