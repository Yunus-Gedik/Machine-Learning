from dataclasses import dataclass
import time
from threading import Thread
from threading import Lock

import pandas as pd
import numpy as np


class bayes:
    freq_table = {}

    def __init__(self, datafile, sep, attr):
        data = pd.read_csv(datafile, sep=sep)
        self.others = np.array(data.drop([attr], 1))
        self.the = np.array(data[attr])

        for attribute in data.columns:
            if attribute != attr:
                self.freq_table[attribute] = {}

        for attribute in data.columns:
            if attribute == attr:
                continue
            temp = np.array(data[attribute])
            for i in range(len(temp)):
                if temp[i] not in self.freq_table[attribute]:
                    self.freq_table[attribute][temp[i]] = [0,0]
                if self.the[i] == 1:
                    self.freq_table[attribute][temp[i]] = [self.freq_table[attribute][temp[i]][0],self.freq_table[attribute][temp[i]][1] + 1]
                else:
                    self.freq_table[attribute][temp[i]] = [self.freq_table[attribute][temp[i]][0] + 1,self.freq_table[attribute][temp[i]][1]]

        self.attr = attr

        # Calculating P(yes) and P(no)
        self.yes_count = 0.0
        self.no_count = 0.0
        for item in self.the:
            if item == 0:
                self.no_count += 1
            else:
                self.yes_count += 1
        self.Pyes = self.yes_count / (self.no_count+self.yes_count)
        self.Pno = 1 - self.Pyes



    def P(self,conditions,guess):
        result = self.Pyes if guess == 1 else self.Pno
        for couple in conditions:
            if guess == 1:
                result *= (self.freq_table[couple[0]][couple[1]][1] / self.yes_count)
            else:
                result *= (self.freq_table[couple[0]][couple[1]][0] / self.no_count)
            result = result / ((self.freq_table[couple[0]][couple[1]][0] + self.freq_table[couple[0]][couple[1]][1]) / (self.yes_count + self.no_count))
        print(result)

b = bayes("dermatology.csv", ",", "family history")

b.P([["oral mucosal involvement",0],["fibrosis of the papillary dermis",0]], 0)











































@dataclass
class Point:
    name: str
    yes: int = 0
    no: int = 0

    def __str__(self):
        return str(self.name) + ',' + str(self.yes) + ',' + str(self.no)


# p = Point("scaling",3,5)
# print(p)






x = 0


def myfunc(i, mutex):
    global x
    while True:
        mutex.acquire(1)
        time.sleep(0.4)
        x += 1
        print("Thread: %d , x = " % i, x)
        mutex.release()
        time.sleep(0.000000001)


"""
mutex = Lock()
for i in range(0, 2):
    t = Thread(target=myfunc, args=(i, mutex))
    t.start()
    print("main loop %d" % i)
"""
