
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


# a really gross function to sort a list of edges in nondecreasing order of the edge weights
def sortEdge(wc_graph):

    sort_graph = []
    sort_graph.append(wc_graph[0])
    least = wc_graph[0]
    for i in range(1, len(wc_graph)):
        val = wc_graph[i][2]
        j = 0
        while val > sort_graph[j][2] and j < len(sort_graph) -1:
            j += 1
        sort_graph.insert(j , wc_graph[i])
        
    temp = sort_graph[len(sort_graph)-1]
    sort_graph.remove(sort_graph[len(sort_graph)-1])
    j = 0
    while temp[2] > sort_graph[j][2] and j < len(sort_graph) -1:
        j += 1
    sort_graph.insert(j , temp)

    return sort_graph


# who's your daddy function
def find(root, parent):

    while root != parent[root]:
        root = parent[root]

    return root
    


def union(parent, rootv, rootu, size):
    
    if(size[rootv] > size[rootu]):
        parent[rootu] = rootv
        
    elif(size[rootv] < size[rootu]):
        parent[rootv] = rootu

    else:
        parent[rootu] = rootv
        size[rootv] += 1



# Kruskal's algorithm for constructing a minimum spanning tree
# Input: A weighted connected graph G = (V,E)
def kurskal(wc_graph):

    MST_list = []   # the empty set to be filled with
                    # the minimum spanning tree of G

    # sort MST_list in nondecreasing order of the edge weights
    sort_graph = sortEdge(wc_graph)

    parent = []     # Stores the root vertex to each vertex
    size = []       # Number of edging dependents to each V

    # initailize each vertex to point to itself
    # and without any dependent edges
    for e in range(vert_cout):
        parent.append(e)
        size.append(0)

    encounter = 0
    k = 0         # initialize the number of processed edges
    while encounter < (vert_cout - 1):
        v = sort_graph[k][0]
        u = sort_graph[k][1]
        k += 1
        rootu = find(v, parent)
        rootv = find(u, parent)
        #if MST_list UNION sort_graph[k] is acyclic:
        if rootv != rootu:
            encounter = encounter +1
            MST_list.append([v, u, sort_graph[k][2]])
            union(parent, rootv, rootu, size)

    return MST_list
    # Output: E_T, the set of edges composing a minimum spanning tree of G



file_name = sys.argv[1]
#file_name = 'city-pairs.txt'

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

# build a weighted complete graph for kurskal's algorithm to run
wc_graph = []
with open(file_name) as f:
   for i in f:
        column = i.strip().split(' ')

        wc_graph.append([
            int(vert_list.index(column[0])),
            int(vert_list.index(column[1])),
            int(column[2])])
f.close()

# run kurskal's algorithm to find the minimum spanning tree
MST_list = kurskal(wc_graph)

# print the results
total = 0
print("The minimum spanning tree is as follows:")
for i in range(len(MST_list)):
    print(vert_list[MST_list[i][0]], " to ", vert_list[MST_list[i][1]], " = ", MST_list[i][2], "miles")
    total += MST_list[i][2]
print("total weight: ", total, " miles.")

# display the results
displayGraph(MST_list)
