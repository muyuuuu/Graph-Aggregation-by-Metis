import numpy as np
import pymetis
import time

def read_data(filename):
    adjacency_list = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            temp = line.split(' ')
            adjacency_list.append(np.array([int(temp[0]), int(temp[1])]))
    return adjacency_list

adjacency_list = read_data('email-Eu-core.txt')
print(len(adjacency_list))

since = time.time()
n_cuts, membership = pymetis.part_graph(100, adjacency=adjacency_list)
end = time.time()

print(end - since)