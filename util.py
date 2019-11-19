"""
The input parser is written in accordance to the specification at 
https://cs170.org/assets/project/spec.pdf
"""
def read_input(filename):
    with open(filename) as f:
        numLocations = int(f.readline())
        numHomes = int(f.readline())
        locations = f.readline().split()
        homes = f.readline().split()
        startLocation = f.readline()

        adjMatrix = []
        for _ in range(numLocations):
            adjMatrix.append(list(f.readline().split()))
        
        graph = Graph(adjMatrix)
    
    return numLocations, numHomes, locations, homes, startLocation, graph

class Graph(object):
    
    """
    preprocess the adjacancy list and get an dictionary representation
    """
    def __init__(self, matrix):
        self.pathFlag = False
        self.matrix = matrix
        self.neighbors = dict()

        for index, row in enumerate(self.matrix):
            self.neighbors[index] = [i for i, j in enumerate(row) if j is not 'x']

    """
    DP algorithm which computes pair-wise shortest paths in O(V^3), which
    can be greatly truncated due to the triangular property
    """
    def initializeShortestPath(self):
        # avoid recomputation
        if self.pathFlag:
            return

        length = len(self.matrix)

        self.shortPath = dict()
        for i in range(length):
            self.shortPath[(i, i)] = 0

       

        indirect = dict()
        for i in range(length - 1):
            indirect[i] = []
            for j in range(i + 1, length):
                if j not in self.neighbors[i]:
                    indirect[i].append(j)
                else:
                    self.shortPath[(i, j)] = self.length(i, j)
        
        for k in range(length):
            for i in range(length):
                for j in indirect[i]:
                    if k != i and k != j:
                        print(i, j, k)
                        tmpDist = self.shortestDist(i, k) + self.shortestDist(k, j)
                        self.shortPath[(i, j)] = min(self.shortPath[(i, j)], tmpDist)

        self.pathFlag = True

    """
    edge length from u to v if there is any edge
    return None if such edge doesn't exist
    """
    def length(self, u, v):
        return self.matrix[u][v]

    def getNeighbor(self, u):
        return self.neighbors[u]
    
    def shortestDist(self, u, v):
        if u < v:
            return self.shortPath[(u, v)]
        else:
            return self.shortPath[(v, u)]

CAR_COST = 1
WALK_COST = 2/3

"""
auto-grading scores for a given solution
"""
def evaluate_output():
    pass

graph = read_input("sample/demo1.in")[-1]
graph.initializeShortestPath()
