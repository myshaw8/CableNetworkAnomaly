import pandas as pd
from IPython.display import display
import os
import matplotlib.pyplot as plt
from numpy import inf
import numpy as np
import json

pd.set_option('display.max_columns', None)

pd_import_list = []
dir = 'data\\fbc'
for file in os.listdir(os.getcwd() + '\\' + dir):
    # print(file)
    print(dir + '\\' + file)
    table = pd.read_csv(dir + '\\' + file)
    N = len(table) #1046
    subset_size = N
    # print(table)
    break
    # pd_import_list.append(pd.read_csv(dir + '\\' + file))
    # print('Loaded {}'.format(file))


def clean_amplitudes(fbc):
    str = fbc.replace(' ','')[1:-1]
    L = str.split(',')
    res = [int(L[i])/100 for i in range(len(L))]
    return res


def distance(fbc1, fbc2, dillution=10):
    n = len(fbc1)
    if n != len(fbc2):
        print("fbcs are different sizes")
        return None
    else:
        d = 0
        for i in range(0,n,dillution):
            d = d + abs(fbc1[i] - fbc2[i])
        return d

def frequencies_vector(df):
    f_indexes = [df["first"][0], df["last"][0], df["span"][0]]
    same = True
    for iter, row in df.iterrows():
        if [row["first"], row["last"], row["span"]] != f_indexes:
            same = False
            break

    if same:
        n = len(df["amplitudes"][0])
        freq = [df["first"][0] + j*df["span"][0] / (n-1) for j in range(n)]
        df["frequencies"] = df.apply(lambda row: freq, axis=1)

    else:
        df.apply(lambda row: [row["first"] + j*row["span"] /(len(row["amplitudes"])-1) for j in range(len(row["amplitudes"]))], axis=1)

def cluster_dist(c1,c2,df):
    d = inf
    for i in c1:
        for j in c2:
            temp = df["distances"][i][j]
            if temp < d:
                d = temp
                idx1, idx2 = i,j
    return d



table = table[["device_id", "span", "first", "last", "amplitudes", "offset"]]
table["amplitudes"] = table["amplitudes"].apply(clean_amplitudes)
frequencies_vector(table)

table["distances"] = table.apply(lambda row: [0 for i in range(N)], axis=1)

table = table.head(subset_size)

L = []
for i, rowi in table.iterrows():
    print(i)
    for j, rowj in table.iterrows():
        if i<j:
            try:
                d = distance(rowi["amplitudes"],rowj["amplitudes"])
                rowi["distances"][j] = d
                rowj["distances"][i] = d
            except:
                print(i,j)
                rowi["distances"][j] = 10**10
                rowj["distances"][i] = 10**10
                if j not in L:
                    L.append(j)
                print(L)

print(table.head())
print(L)
# print(len(table))


clusters = [[i] for i in range(subset_size)]
k = 5

n_clusters = len(clusters)
cluster_distances = np.array([[inf for i in range(len(clusters))] for i in range(len(clusters))])
for i in range(n_clusters):
    clusteri = clusters[i]
    dist = [0 for i in range(n_clusters)]
    for j in range(i):
        clusterj = clusters[j]
        d = cluster_dist(clusteri,clusterj,table)
        cluster_distances[i][j] = d
        cluster_distances[j][i] = d

for count in range(n_clusters-k):
    d_min = np.amin(cluster_distances)
    i_min, j_min = np.where(cluster_distances == d_min)[0]

    clusters[i_min] = clusters[i_min]+clusters[j_min]
    clusters[j_min] = []
    for i in range(n_clusters):
        cluster_distances[i][j_min] = inf
        cluster_distances[j_min][i] = inf


clusters = [[table["device_id"][i] for i in x] for x in clusters if x!= []]
print(clusters)

with open('cluster_result', 'w') as f:
    json.dump(clusters, f)
