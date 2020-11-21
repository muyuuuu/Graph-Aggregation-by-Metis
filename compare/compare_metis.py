import networkx as nx
import metis
import time

g = nx.read_adjlist("email-Eu-core.txt", nodetype=int)  

def createGraph(filename) :
    G = nx.Graph()
    for line in open(filename) :
        strlist = line.split()
        n1 = int(strlist[0])
        n2 = int(strlist[1])
        G.add_edges_from([(n1, n2)])
    return G

g = createGraph("email-Eu-core.txt")
metis.networkx_to_metis(g)

def read_data(filename):
    adj_list = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            temp = line.split(' ')
            # max_v = max(max_v, int(temp[0]), int(temp[1]))
            adj_list.append((int(temp[0]), int(temp[1])))
    return adj_list

adjlist = read_data('email-Eu-core.txt')

g = metis.adjlist_to_metis(adjlist)

since = time.time()
(edgecuts, parts) = metis.part_graph(g, 3)
end = time.time()

print(end-since)