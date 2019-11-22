import math, random
import string
import numpy as np
from util import read_input

"""
Edit this config (or create a new config) to control the output sample
"""
def rand_locations(n, length):
    locs = set()
    while len(locs) != n:
        strs = [random.choice(string.ascii_lowercase) for _ in range(length)]
        locs.add(''.join(strs))
    return list(locs)

DEFAULT_CONFIG = {
    "file_name" : "./sample/50.in",
    "loc_num" : 50,
    "home_num" : 25,
    "connectivity" : 0.3, 
    "rand_method" : rand_locations
}

def generate_input(config=DEFAULT_CONFIG):
    loc_num = config["loc_num"]
    home_num = config["home_num"]
    method = config["rand_method"]
    connectivity = config["connectivity"]
    length = math.ceil((math.log10(loc_num)))
    
    locations = method(loc_num, length)

    home_locs = set()
    while len(home_locs) != home_num:
        home_locs.add(random.choice(locations))
    home_locs = list(home_locs)

    start_loc = random.choice(locations)

    metricPos = dict()

    for i in range(loc_num):
        metricPos[i] = randomPoints()
    
    edgeMat = np.zeros(shape=(loc_num, loc_num))

    for i in range(loc_num - 1):
        for j in range(i + 1, loc_num):
            coin = random.random()
            # connectivity controls how many edges should be established
            if coin < connectivity:
                edgeMat[i][j] = euclideanDist(metricPos[i], metricPos[j])
            else:
                edgeMat[i][j] = 0.0

    for i in range(loc_num - 1):
        for j in range(i, loc_num):
            edgeMat[j][i] = edgeMat[i][j]
    
    with open(config["file_name"], 'w') as f:
        f.write(str(loc_num) + '\n')
        f.write(str(home_num) + '\n')
        f.write(' '.join(locations) + '\n')
        f.write(' '.join(home_locs) + '\n')
        f.write(start_loc + '\n')
        for row in np.ndarray.tolist(edgeMat):
            strRow = [str(i) if i != 0 else 'x' for i in row]
            f.write(' '.join(strRow) + '\n')

def generate_output(filename):
    numLocations, numHomes, locations, homes, startLocation, graph = read_input(filename)
    visited = []

    start = graph.locNames[startLocation]
    visited.append(start)
    backup = start
    numVisist = random.randint(3, numLocations // 2)
    i = 1

    while i < numVisist:
        start = random.choice(graph.getNeighbor(start))
        visited.append(start)
        i += 1
    
    while start != backup:
        i += 1
        if backup in graph.getNeighbor(start):
            visited.append(backup)
            break
        else:
            start = random.choice(graph.getNeighbor(start))
            visited.append(start)

    dropLocs = list(set([random.choice(visited[1:i-2]) for _ in range(i // 2)]))
    dropLocDict = {}

    for loc in dropLocs:
        dropLocDict[loc] = []
        r = random.choice(homes)
        homes.remove(r)
        dropLocDict[loc].append(r)

    while len(homes) != 0:
        loc = random.choice(dropLocs)
        r = random.choice(homes)
        homes.remove(r)
        dropLocDict[loc].append(r)
    
    filePrefix = filename[:-3]
    outputFileName = filePrefix + ".out"

    print(visited)
    print(dropLocDict)

    with open(outputFileName, 'w') as f:
        f.write(' '.join(list(map(graph.indexToName, visited))) + '\n')
        f.write(str(len(dropLocs)) + '\n')
        for loc in dropLocDict:
            lst = dropLocDict[loc]
            lst.insert(0, graph.indexToName(loc))
            f.write(' '.join(lst) + '\n')
    

def randomPoints():
    return (random.randint(0, 100), random.randint(0, 100))

def euclideanDist(u, v):
    return round(math.sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2), 5)

