from abc import abstractmethod


class GraphInterface:
    @abstractmethod
    def addNode(self, node):
        pass

    @abstractmethod
    def addEdge(self, v1, v2):
        pass

    @abstractmethod
    def deleteNode(self, node):
        pass

    @abstractmethod
    def deleteEdge(self, v1, v2):
        pass

    @abstractmethod
    def getAdjacentNodes(self, v1):
        pass

    @abstractmethod
    def getAdjacentEdges(self, v1, v2):
        pass
