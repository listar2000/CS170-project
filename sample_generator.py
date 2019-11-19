import math, random
import string
import numpy as np

def rand_locations(n, length):
    locs = set()
    while len(locs) != n:
        strs = [random.choice(string.ascii_lowercase) for _ in range(length)]
        locs.add(''.join(strs))
    return list(locs)

DEFAULT_CONFIG = {
    "file_name" : "demo2.in",
    "loc_num" : 40,
    "home_num" : 20,
    "connectivity" : 0.5, 
    "rand_method" : rand_locations
}

def generate_input(config=DEFAULT_CONFIG):
    loc_num = config["loc_num"]
    home_num = config["home_num"]
    method = config["rand_method"]
    length = math.ceil((math.log10(loc_num)))
    
    locations = method(loc_num, length)
    home_locs = [random.choice(locations) for i in range(home_num)]
    start_loc = random.choice(locations)

    metricPos = dict()

    for i in range(loc_num):
        metricPos[i] = randomPoints()
    
    edgeMat = np.zeros(shape=(loc_num, loc_num))

    for i in range(loc_num - 1):
        for j in range(i + 1, loc_num):
            edgeMat[i][j] = euclideanDist(metricPos[i], metricPos[j])

    for i in range(loc_num - 1):
        for j in range(i, loc_num):
            edgeMat[j][i] = edgeMat[i][j]
    
    print(edgeMat)

def randomPoints():
    return (10 * random.random(), 10 * random.random())

def euclideanDist(u, v):
    return round(math.sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2), 2)

