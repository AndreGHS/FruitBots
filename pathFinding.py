import collections

class Graph:

    def __init__(self):
        self.nodes = list()
        self.edges = collections.defaultdict(list)
        self.positions = collections.defaultdict(int)


    def add_node(self, value):
        self.nodes.append(value)

    def add_edge(self, from_node, to_node):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)

    def setPosition(self, node, boardPosition):
        self.positions[node] = boardPosition

    def constructGraphFromGrid(self, gridSize):
        node_index = 0
        for row in range(0, gridSize):
            for column in range(0, gridSize):
                self.add_node(str(row) + str(column))
                self.setPosition(str(row) + str(column), [row, column])
                if(column < gridSize - 1):
                   if node_index + 1 < pow(gridSize, 2):
                        self.add_edge(str(row) + str(column), str(row) + str(column + 1))
                if node_index + gridSize < pow(gridSize, 2):
                    self.add_edge(str(row) + str(column), str(row + 1) + str(column))

                node_index += 1
                
    def getPathForMovement(self, shortestPath):
        shortestPath.pop(0)
        pathToMove = list()
        for node in shortestPath:
            pathToMove.append(self.positions[node])
        return pathToMove

    def bfs_short_path(self, startNode, target):

        isStartNode = True
        exploredNodes = list()
        queue = list()
        queue.append(startNode)

        while queue:
            path = queue.pop(0)
            if isStartNode:
                node = path
            else:
                node = path[-1]

            if node not in exploredNodes:
                neighbours = self.edges[node];

                for neighbour in neighbours:
                    if isStartNode:
                        new_path = list()
                        new_path.append(path)
                    else:
                        new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    if neighbour == target:
                        return new_path
                isStartNode = False
                exploredNodes.append(node)

g = Graph()

g.constructGraphFromGrid(5)
print(g.nodes)
print(g.edges)
sp = g.bfs_short_path('21', '34')
print (sp)
print(g.getPathForMovement(sp))

