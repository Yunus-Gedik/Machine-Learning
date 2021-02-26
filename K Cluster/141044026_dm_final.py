# Python 3.7.8

import math
import random
import pandas as pd
import numpy as np

# fills k clusters with appropriate data points
def cluster_filler(ks,data_arr):
    clusters = [[] for i in range(len(ks))]

    for item in data_arr:

        # appropriate() item into a cluster
        index = appropriate(ks,item)

        # Add item to cluster
        clusters[index].append(item)

    return clusters

# Finds min distance mean
def appropriate(mean,item):

    index = -1
    minimum = distance(item, mean[0])
    index = 0
    for i in range(len(mean)):
        # Find distance from item to mean
        k_item_distance = distance(item, mean[i])

        if k_item_distance < minimum:
            minimum = k_item_distance
            index = i

    return index

# find actual ks
def kCluster(dataFile,sep,k):
    data = pd.read_csv(dataFile, sep=sep)
    data_arr = np.array(data)

    minn, maxx = kBound(data_arr)
    ks = kMeanPoints(data_arr,k,minn,maxx)
    clusters = [0 for i in range(len(ks))]


    for i in range(len(data_arr)):

        item = data_arr[i]

        # appropriate() item into a cluster and update the
        # corresponding means.
        index = appropriate(ks,item)

        clusters[index] += 1
        cSize = clusters[index]
        ks[index] = newMeanPoint(cSize,ks[index],item)

    return ks, data_arr



# Euclidean distance
def distance(a, b):
    dist = 0.0
    for i in range(len(b)):
        dist = dist + math.pow(a[i] - b[i], 2)
    return math.sqrt(dist)

# find boundaries for random k position at the beginning
def kBound(data):
    n = len(data[0])
    minn = [None] * n
    maxx = [None] * n

    for f in range(n):
        minn[f] = data[0][f]
        maxx[f] = data[0][f]

    for item in data:
        for f in range(len(item)):
            if item[f] < minn[f]:
                minn[f] = item[f]

            if item[f] > maxx[f]:
                maxx[f] = item[f]

    return minn,maxx

# create random k mean points
def kMeanPoints(data,k,bound_x,bound_y):
    f = len(data[0])
    points = [[0 for i in range(f)] for j in range(k)];

    for mean in points:
        for i in range(len(mean)):
            mean[i] = random.uniform(bound_x[i], bound_y[i])

    np.random.shuffle(points)

    return points

# updates a means' position with new data
def newMeanPoint(numbers_included, mean, new):
    for i in range(len(mean)):
        att = mean[i]
        att = (att*(numbers_included-1)+new[i])/float(numbers_included)
        mean[i] = round(att, 3)
    return mean


def printer(cs):
    for item in cs:
        for i in range(len(item)):
            item[i] = item[i].tolist()
        print(item)


def kmeanscluster(dataFile,sep,k):
    ks, data_arr = kCluster(dataFile,sep,k)
    np.random.shuffle(data_arr)
    cs = cluster_filler(ks,data_arr)

    #printer(cs)

    return cs


def find_k(dataFile,sep):
    arr = []
    css = []
    for i in range(1,10):
        temp = kmeanscluster(dataFile,sep,i)
        css.append(temp)
        arr.append(0)
        for item in temp:
            if item:
                arr[i-1] += 1

    temp =[]
    for i in range(1,8):
        temp.append(arr[i-1] / arr[i+1])

    print("Best k value is:")
    print(temp.index(min(temp))+1)

    print("Clusters are:")
    final = kmeanscluster(dataFile,sep,temp.index(min(temp))+1)
    printer(final)

#kmeanscluster("buddymove_holidayiq.csv",",")
find_k("buddymove_holidayiq.csv",",")
