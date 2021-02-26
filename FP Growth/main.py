import csv


def read_order(file_name, threshold):
    freq = {}
    data = csv.reader(open(file_name), delimiter=',')

    # calculate all frequency
    for line in data:
        for item in line:
            if item in freq:
                freq[item] += 1
            else:
                freq[item] = 1

    # remove lower frequency then threshold
    filter_freq = {}

    for item in freq.items():
        # print(item)
        if item[1] >= threshold:
            filter_freq[item[0]] = item[1]

    del freq

    # remove unwanted attributes from data
    datalist = []
    data = csv.reader(open(file_name), delimiter=',')
    for line in data:
        datalist.append(line)

    for line in datalist:
        temp = []
        for item in line:
            if item not in filter_freq:
                temp.append(item)
        for item in temp:
            line.remove(item)

    # remove empty lists from data
    i = 0
    while i < len(datalist):
        if len(datalist[i]) == 0:
            del datalist[i]
            i -= 1
        i += 1

    # sort each data line respect to frequency in descending order
    for line in datalist:
        # continue
        # print(line)
        line.sort(reverse=True, key=(lambda x: filter_freq[x]))

    # sort frequencies in descending order
    sorted_freq = sorted(filter_freq.items(), key=lambda item: (-item[1], item[0]))

    return datalist, filter_freq, sorted_freq


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = []

    def inc(self):
        self.count += 1

    # add a child
    def birth(self, child):
        self.children.append(child)

    # check if there is a child named childName
    def childCheck(self, childName):
        for child in self.children:
            if child.name == childName:
                return child
        return None

    # print all dynasty
    def visualize(self, ind=0):
        print('-- ' * ind, self.name, ' ', self.count)
        for child in self.children:
            child.visualize(ind + 1)

    # keep track of every object of an specific child name
    def connect(self, conPat):
        if self.name not in conPat:
            conPat[self.name] = []
        conPat[self.name].append(self)
        for item in self.children:
            item.connect(conPat)

# From data, construct tree
def construct(root, line):
    if len(line) == 0:
        return

    child = root.childCheck(line[0])
    if child is not None:
        child.inc()
        construct(child, line[1:len(line)])
    else:
        newBorn = treeNode(line[0], 1, root)
        root.birth(newBorn)
        construct(newBorn, line[1:len(line)])


# From data, construct a leaf with count value,
# this function is using for creating FP tree from conditional pattern base
def constructLeaf(root, line, value):
    if len(line) == 0:
        return

    child = root.childCheck(line[0])
    if child is not None:
        if len(line) == 1:
            child.count += value
        else:
            child.inc()
        constructLeaf(child, line[1:len(line)],value)
    else:
        if len(line) == 1:
            newBorn = treeNode(line[0], value, root)
        else:
            newBorn = treeNode(line[0], 1, root)
        root.birth(newBorn)
        constructLeaf(newBorn, line[1:len(line)],value)


# From a leaf node object, by tracking until there is no parent
# creates a list of visited objects names.
def conFP(conData, item):
    if item.parent is None:
        return
    conData.insert(0,item.name)
    conFP(conData,item.parent)








# Get data, filtered frequency as dict, and sorted frequency as list
data, filter_freq, sorted_freq = read_order("groceries.csv", 0)

# print(data)
# print(filter_freq)
# print(type(sorted_freq))

# Create a root
root = treeNode("rootNode", 1, None)

# fetch all data to tree
for line in data:
    construct(root, line)

# Shows constructed tree in terminal
root.visualize()

print("\n\n\n\n\n\n\n\n\n\n\n\n")



conPat = {}
root.connect(conPat)        # Saves all related objects with attributes. i.e. saves all "milk" objects in the tree to conPat["milk"]
del conPat["rootNode"]      # rootNode is not an attribute so delete it.



# From conditional pattern base create fp trees.
# Least frequent one is first
for i in range(len(sorted_freq)-1,-1,-1):
    conRoot = treeNode("rootNode", 1, None)
    line = conPat[sorted_freq[i][0]]        # Fetch all the leaf objects for a specific attribute into "line"
    for item in line:                       # Her bir obje için
        conData = []
        conFP(conData,item)                 # Bottom up read names
        conValue = item.count               # Saves leaf value
        constructLeaf(conRoot,conData,conValue)      # Adds to tree
    conRoot.visualize()
    pass











