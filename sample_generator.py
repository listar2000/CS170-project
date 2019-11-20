import math, random
import string
import numpy as np

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
    "file_name" : "./sample/demo2.in",
    "loc_num" : 40,
    "home_num" : 20,
    "connectivity" : 0.5, 
    "rand_method" : rand_locations
}

def generate_input(config=DEFAULT_CONFIG):
    loc_num = config["loc_num"]
    home_num = config["home_num"]
    method = config["rand_method"]
    connectivity = config["connectivity"]
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

def randomPoints():
    return (10 * random.random(), 10 * random.random())

def euclideanDist(u, v):
    return round(math.sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2), 2)

if __name__ == '__main__':
    generate_input()

