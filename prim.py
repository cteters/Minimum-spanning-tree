#!/usr/bin/python

import matplotlib.pyplot as plt
import networkx as nx
import sys

'''
For the program to work, install the following software:

sudo apt-get install python3-tk 
sudo pip3 install networkx
sudo pip3 install matplotlib

Or with O.S. specific information and run as a Python3 file.
example: python3 prim.py city-pairs.txt
'''

def displayGraph(MST_list):
    # create a graph to image
    G = nx.Graph()

    for i in range(len(MST_list)): 
        G.add_edge(
                vert_list[MST_list[i][0]],
                vert_list[MST_list[i][1]],
                weight=int(MST_list[i][2]))

    edge=[(u,v) for (u,v,d) in G.edges(data=True)]
    
    # node position format
    pos=nx.spring_layout(G, k=20, pos=None, fixed=None, iterations=150, weight='weight', scale=1.0)
    #pos=nx.graphviz_layout(G, prog='dot') 
    #graphviz would be a much cooler position format, that uses tree branching

    # weights
    weight = dict(map(lambda x:((x[0],x[1]), str(x[2]['weight'] ) ), G.edges(data = True)))
    nx.draw_networkx_edge_labels(G, pos, edge_labels = weight)

    # finds the longest node name to scale nodes to size of text
    node_len = 0
    for i in range(vert_cout):
        if len(vert_list[i]) > node_len:
            node_len = len(vert_list)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=node_len * 180, node_shape='h', node_len=100, alpha=0.5)
    # other node_shape to try:   so^>v<dph8 

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=edge, width=2, edge_color='b', alpha=0.5)

    # labels
    nx.draw_networkx_labels(G, pos, font_size=9, font_family='sans-serif')

    plt.axis('off')
    plt.show()



# Prim's Algorithm for constructing a minimum spanning tree
# Input: A weighted connected graph G = V, E
def prim(wc_graph):
  
    MST_list = []       # the empty set to be filled with
                        # the minimum spanning tree of G

    visited_list = []   # a list of all visited verticese

    edge_list = []      # stores edges worth considering
                        # as minimum-weight edge

    # minimum-weight edge to actually be use
    min_edge = [0, 1, wc_graph[0][1]] # [v, u, weight]

    v = 0
    for V in range(vert_cout-1):
    
        # add current vertex to the visited list
        visited_list.append(v)
    
        # updated the edge list with every current
        # candidate that can be a minimum-weight edge
        for u in range(vert_cout):
            if wc_graph[v][u] != 0:
                edge_list.append([v, u, wc_graph[v][u]])
        
        # find a minimum-weight edge among all the edge candidates
        for e in range(1, len(edge_list)):
            if edge_list[e][2] < min_edge[2] and edge_list[e][1] not in visited_list:
                min_edge = edge_list[e]

        # updated the MST list with the discovered minimum-weight edge
        MST_list.append(min_edge)
      
        v = min_edge[1] # traverse to next vertex

        # remove the used minimum-weight edge
        edge_list.remove(min_edge)
        min_edge = edge_list[0]

    return MST_list
    # Output: The empty set filled with the minimum spanning tree of G



# store argument from terminal
# example: python3 prim.py city-pairs.txt
file_name = sys.argv[1]

# collects a set of all vertices to avoid duplicates
vert_set = set()
with open(file_name) as f:
   for i in f:
       column = i.strip().split(' ')
       vert_set.add(column[0])
       vert_set.add(column[1])
f.close()

vert_list = list(vert_set)    # converts the set to a list
vert_cout = (len(vert_set))   # maintain a count of all vertices

# Build a 2D array to hold the weighted complete graph
# of entry data, with a width and height equal to 'vert_cout'
wc_graph = [[0 for i in range(vert_cout)] for j in range(vert_cout)]

# Fill 2D array that represents wieghted complete graph  with
# all entry data found in 'file_name'
with open(file_name) as f:
   for i in f:
       column = i.strip().split(' ')
       wc_graph[int(vert_list.index(column[0]))][int(vert_list.index(column[1]))]=int(column[2])
f.close()

# run prim's algorithm to find the minimum spanning tree
MST_list =  prim(wc_graph)

# print the results
total = 0
print("The minimum spanning tree is as follows:")
for i in range(len(MST_list)):
    print(vert_list[MST_list[i][0]], " to ", vert_list[MST_list[i][1]], " = ", MST_list[i][2], "miles")
    total += MST_list[i][2]
print("total weight: ", total, " miles.")

#display the results
displayGraph(MST_list)
