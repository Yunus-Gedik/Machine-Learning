import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import math
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style
from sklearn.neighbors import KNeighborsClassifier

data = pd.read_csv("student-mat.csv", sep=";")

#print(len(data))

data = data[["G1", "G2", "G3", "studytime", "failures", "absences", "freetime"]]

predict = "G3"

X = np.array(data.drop([predict], 1))
Y = np.array(data[predict])

x_train,x_test,y_train,y_test = sklearn.model_selection.train_test_split( X,Y, test_size = 0.1 )

# print(len(sklearn.model_selection.train_test_split( X,Y, test_size = 0.1 )))

"""
model = KNeighborsClassifier(n_neighbors=5)
model.fit(x_train,y_train)

acc = model.score(x_test,y_test)

print(acc)
"""

linear = linear_model.LinearRegression()

linear.fit(X,Y)
acc = linear.score(x_test, y_test)

print("Regression accuracy")
print(acc,"\n")


with open("studentmodel.pickle", "wb") as f:
    pickle.dump(linear, f)

reload = open("studentmodel.pickle", "rb")
linear = pickle.load(reload)



predictions = linear.predict(x_test)

correct = 0.0

for i in range (len(predictions)):
    f = math.floor(predictions[i])
    c = math.ceil(predictions[i])
    predictions[i] = f if abs(f)-predictions[i] < abs(c)-predictions[i] else c

    if predictions[i] == y_test[i]:
        correct += 1
print("Classification of regression prediction accuracy")
print(correct / len(predictions))

    #print(final, y_test[i])


p = "G2"
style.use("ggplot")
pyplot.scatter(data[p], data["G3"])
pyplot.xlabel(p)
pyplot.ylabel("Final Grade")
pyplot.show()


"""
print( len(x_test)  )
print(x_test)
print("------------------------------------------------")
print( len(x_train))
print(x_train)
print("------------------------------------------------")

print( len(y_test))
print(y_test)
print("------------------------------------------------")
print( len(y_train))
print(y_train)
print("------------------------------------------------")

"""