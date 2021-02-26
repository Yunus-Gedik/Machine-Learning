# Python 3.7.8

import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as pyplot

# DB-Scan implementation which explained in the book
def dbscan(D, radius, minPts):
    rand = []

    clusters = []

    # Random order
    for i in range(len(D)):
        rand.append([i])
    random.shuffle(rand)

    # mark all data point as unvisited and does not belong to any cluster
    for i in range(len(rand)):
        rand[i].append(0)
        rand[i].append(0)
        rand[i].append(0)



    # D.append(rand)
    # print(D)

    for i in range(len(D)):
        if rand[i][1] == 1 or rand[i][3] == 1:
            continue

        # Mark visited
        else:
            rand[i][1] = 1

        N = []
        if hood(D, radius, minPts, rand[i][0], rand, N):
            newCluster = []
            newCluster.append(D[rand[i][0]])
            rand[i][2] = 1

            m = 0

            while m < len(N):
                if rand[N[m]][1] == 0:
                    rand[N[m]][1] = 1

                    enlarge = []
                    if hood(D, radius, minPts, rand[N[m]][0], rand, enlarge):
                        N = np.append(N,enlarge)
                        N = np.unique(N)
                        m = 0
                        continue
                if rand[N[m]][2] == 0:
                    newCluster.append(D[rand[N[m]][0]])
                    rand[N[m]][2] = 1
                m += 1
            newCluster = np.unique(newCluster,axis=0).tolist()
            clusters.append(newCluster)
        else:
            rand[i][3] = 1

    return clusters

# Checks if there are enough number of neighbors around a point and saves that points to N.
def hood(D, radius, minPts, point, rand, N):
    N.clear()

    for i in range(len(rand)):
        if distance(D[point], D[rand[i][0]], len(D[point])) <= radius:
            N.append(i)

    if len(N) >= minPts:
        return True
    return False

# Calculate the distances between two points
def distance(a, b, size):
    dist = 0.0
    for i in range(size):
        dist = dist + math.pow(a[i] - b[i], 2)
    return math.sqrt(dist)

# Reads data from .csv file and picks 2 attributes then performs DB-Scan on that data. Then visualizes it and
# prints clusters to terminal.
def dbscan_print(dataFile,sep,c0,c1,radius,minPts):
    data = pd.read_csv(dataFile, sep=sep)
    data = data[[c0, c1]]

    a = dbscan(np.array(data), radius, minPts)

    pyplot.xlabel(c0)
    pyplot.ylabel(c1)

    # print each cluster
    for i in range(len(a)):
        print(a[i])
        b = pd.DataFrame(a[i],columns=[c0,c1])
        pyplot.scatter(b[c0], b[c1])

    print(len(a)," clusters extracted.")

    pyplot.show()


# Revised from CMU StatLib library, data concerns city-cycle fuel consumption.
#dbscan_print("auto-mpg.csv",",","weight","displacement",40,6)

# Abalones' physical measurements.
#dbscan_print("abalone.csv",",","rings","whole_w",1,15)

# User interest information extracted from user reviews published in holidayiq.com about various types of point of interests in South India.
dbscan_print("buddymove_holidayiq.csv",",","Nature","Theatre",10,5)
