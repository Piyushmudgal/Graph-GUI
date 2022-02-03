#author Piyush Mudgal
from GraphInterface import GraphInterface


class Graph(GraphInterface):
    _graph = {}  # Private Variable created by the use of '_'

    # Function to add a New Node to Graph
    def addNode(self, node):
        if node not in self._graph:
            self._graph[node] = []

    # Function to add New Edge to Graph
    def addEdge(self, v1, v2):
        if v1 not in self._graph or v2 not in self._graph:
            return False
        self._graph[v1].append(v2)
        self._graph[v2].append(v1)

    # Function to Delete a Pre-existing Node
    def deleteNode(self, node):
        if node not in self._graph:
            return False
        del self._graph[node]
        for i in self._graph:
            for j in self._graph[i]:
                if j == node:
                    self._graph[i].remove(j)

    # Function to Delete a Pre-Existing Edge
    def deleteEdge(self, v1, v2):
        if v1 not in self._graph or v2 not in self._graph or v2 not in self._graph[v1] or v1 not in self._graph[v2]:
            return False
        self._graph[v1].remove(v2)
        self._graph[v2].remove(v1)

    # Function to Get Adjacent Node of a Node
    def getAdjacentNodes(self, v1):
        if v1 not in self._graph:
            return False
        for i in self._graph[v1]:
            print(i, end=" ")
        print()

    # Function to get Adjacent Edges of an Edge
    def getAdjacentEdges(self, v1, v2):
        if v1 not in self._graph or v2 not in self._graph:
            return False
        l = []
        for i in self._graph[v1]:
            if i == v2:
                continue
            l.append((v1, i))
        for i in self._graph[v2]:
            if i == v1:
                continue
            l.append((v2, i))
        return tuple(l)

    def BFS(self, start, destination):
        if start not in self._graph or destination not in self._graph:
            return False
        visited = {}  # Dictionary to maintain a note of visited Nodes
        for i in self._graph:
            visited[i] = 0
        parent = {}  # Dictionary to backtrack and find the route
        # And the no of steps needed to get to Destination Node from Start Node
        for i in self._graph:
            parent[i] = None
        Queue = [start]  # Queue used for BFS
        visited[start] = 1
        parent[start] = -1
        while Queue:
            current = Queue.pop(0)
            if current == destination:
                break
            for i in self._graph[current]:
                if visited[i] == 0:
                    Queue.append(i)
                    visited[i] = 1
                    parent[i] = current

        cur = destination
        distance = 0
        path = []
        while parent[cur] != -1:
            path.append(cur)
            distance += 1
            cur = parent[cur]
        path.append(start)
        path.reverse()
        return path

    #author Desharaju Sai Abhishek
    def DFS(self, start, dest):
        stack = [[start]]
        visited = [0]
        while stack:
            path = stack.pop(0)
            node = path[-1]
            if node == dest:
                return path
            children = self._graph[node]
            for child in children:
                if child not in visited:
                    newPath = path + [child]
                    stack.insert(0, newPath)
                    visited.append(child)

    @property
    def graph(self):
        return self._graph
