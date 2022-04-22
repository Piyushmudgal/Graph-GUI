from time import time, sleep

from Graph import Graph
import turtle
from math import sqrt
import pandas as pd


class Stats:
    def __init__(self):
        self.count = 0
        self.last_update = time()
        self.head = turtle.Turtle()
        self.head.pu()
        self.head.hideturtle()

    def show_fps(self):
        self.count += 1
        if self.count >= 100000000:
            self.count = 100
            self.last_update = time()
        self.head.clear()
        fps = round(self.count / (time() - self.last_update + 1), 2)
        self.head.goto(-460, 380)
        self.head.write(str(fps), True, font=('Arial', 10, 'normal'))


class Node:
    id = 0
    NODE_SIZE = 12
    FONT_SIZE = 10

    def __init__(self, x, y, tur):
        self.id = Node.id
        Node.id += 1
        self.x = x
        self.y = y
        self.selected = False

        self.turtle = turtle.Turtle()
        # self.turtle = tur
        self.turtle.hideturtle()
        self.turtle.penup()

    def clear(self):
        self.turtle.clear()

    def draw(self):
        if self.selected:
            self.turtle.color("green")
        else:
            self.turtle.color("#ffffff")

        self.turtle.goto(self.x, self.y)
        self.turtle.pensize(Node.NODE_SIZE)
        self.turtle.dot()

        self.turtle.goto(self.x, self.y - Node.FONT_SIZE)
        self.turtle.color("black")
        # self.turtle.write(str(self.id), True, font=("Arial", Node.FONT_SIZE, "normal"))

    def exist(self, x, y):
        dis = sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        if dis < Node.NODE_SIZE:
            return True
        return False


class Edge:
    EDGE_SIZE = 8

    def __init__(self, n1: Node, n2: Node, tur):
        self.n1 = n1
        self.n2 = n2
        self.selected = False

        # self.turtle = tur
        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.turtle.speed(0)

    def draw(self):
        if self.selected:
            self.turtle.color("blue")
        else:
            self.turtle.color("black")

        self.turtle.pensize(Edge.EDGE_SIZE)
        self.turtle.pu()
        self.turtle.goto(self.n1.x, self.n1.y)
        self.turtle.pd()
        self.turtle.goto(self.n2.x, self.n2.y)
        self.turtle.pu()

    def clear(self):
        self.turtle.clear()

    def exist(self, x, y):
        try:
            m = (self.n2.y - self.n1.y) / (self.n2.x - self.n1.x)
        except ZeroDivisionError:
            m = (self.n2.y - self.n1.y) / float("-inf")
        a = m
        b = -1
        c = self.n1.y - (m * self.n1.x)

        length = sqrt((self.n2.x - self.n1.x) ** 2 + (self.n2.y - self.n1.y) ** 2)
        distance_from_line = abs(a * x + b * y + c) / sqrt(a ** 2 + b ** 2)
        center_x = (self.n2.x + self.n1.x) / 2
        center_y = (self.n2.y + self.n1.y) / 2
        distance_from_center = sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        if distance_from_line < Edge.EDGE_SIZE and distance_from_center <= length / 2:
            return True
        return False


class GraphGui:
    def __init__(self, screen):
        self.graph = Graph()
        self.nodes = {}
        self.edges = {}

        self.turtle = turtle.Turtle()
        self.turtle.hideturtle()
        self.screen = screen

        self.busy = False  # tells if the class is working on a function
        self.selected_node = None
        self.selected_edge = None

        self.stats = Stats()

    # author Subhadip Nandi
    def _create_node(self, x, y):
        # if len(self.nodes) % 3 == 0:
        #     self.turtle = turtle.Turtle()
        #     self.turtle.hideturtle()
        new_node = Node(x, y, self.turtle)
        self.graph.addNode(new_node.id)
        self.nodes[new_node.id] = new_node
        return new_node.id

    # author Subhadip Nandi
    def _create_edge(self, n1, n2):
        if n1.id > n2.id:
            temp = n1
            n1 = n2
            n2 = temp
        new_edge = Edge(n1, n2, self.turtle)
        weight = turtle.numinput("Edge Weight", "Enter edge weight")
        # weight = 5
        self.graph.addEdge(n1.id, n2.id, weight)
        self.edges[str(n1.id) + ',' + str(n2.id)] = new_edge
        turtle.listen()

    # author Subhadip Nandi
    def delete(self):
        if self.selected_node is not None:
            self.graph.deleteNode(self.selected_node)
            to_delete = []
            for k in self.edges:
                if str(self.selected_node) in k:
                    to_delete.append(k)
            for k in to_delete:
                self.edges[k].clear()
                del self.edges[k]
            self.nodes[self.selected_node].clear()
            del self.nodes[self.selected_node]
            self.selected_node = None
            return
        if self.selected_edge is not None:
            self.graph.deleteEdge(int(self.selected_edge.split(",")[0]), int(self.selected_edge.split(",")[1]))
            self.edges[self.selected_edge].clear()
            del self.edges[self.selected_edge]
            self.selected_edge = None

        turtle.onscreenclick(self.on_left_click, 1, True)
        turtle.listen()

    def edge_exist(self, id1, id2):
        if id1 > id2:
            temp = id1
            id1 = id2
            id2 = temp
        if str(id1) + ',' + str(id2) in self.edges.keys():
            return True
        return False

    def on_left_click(self, x, y):
        if self.busy:
            return

        clicked_node = None
        for k in self.nodes.keys():
            if self.nodes[k].exist(x, y):
                clicked_node = k

        clicked_edge = None
        for k in self.edges.keys():
            if self.edges[k].exist(x, y):
                clicked_edge = k

        if clicked_node is None:
            if clicked_edge is None:
                node_id = self._create_node(x, y)
                if self.selected_node is not None:
                    self.nodes[self.selected_node].selected = False
                    self._create_edge(self.nodes[self.selected_node], self.nodes[node_id])
                self.selected_node = node_id
                self.nodes[node_id].selected = True
        else:
            if clicked_node == self.selected_node:
                self.nodes[clicked_node].selected = False
                self.selected_node = None
            else:
                if self.selected_node is not None:
                    if not self.edge_exist(self.selected_node, clicked_node):
                        self._create_edge(self.nodes[self.selected_node], self.nodes[clicked_node])
                    self.nodes[self.selected_node].selected = False
                if self.selected_edge is not None:
                    self.edges[self.selected_edge].selected = False
                self.nodes[clicked_node].selected = True
                self.selected_node = clicked_node
            return

        if clicked_edge is None:
            pass
        else:
            if clicked_edge == self.selected_edge:
                self.edges[clicked_edge].selected = False
                self.edges[self.selected_edge].selected = False
                self.selected_edge = None
            else:
                if self.selected_node is not None:
                    self.nodes[self.selected_node].selected = False
                if self.selected_edge is not None:
                    self.edges[self.selected_edge].selected = False
                self.edges[clicked_edge].selected = True
                self.selected_edge = clicked_edge
            return

    def bfs(self):
        self.busy = True
        try:
            starting_node = int(turtle.numinput("Starting node", "Enter Starting node: ", 0))
            to_find = int(turtle.numinput("End Node", "Which node to find", 0))
        except TypeError:
            self.busy = False
            return

        order = self.graph.BFS(starting_node, to_find)

        if self.selected_node is not None:
            self.nodes[self.selected_node].selected = False
            self.selected_node = None
        if self.selected_edge is not None:
            self.edges[self.selected_edge].selected = False
            self.selected_edge = None

        for i in order[0]:
            self.selected_node = i
            self.nodes[self.selected_node].selected = True
            for k in self.edges.keys():
                self.edges[k].draw()
            for k in self.nodes.keys():
                self.nodes[k].draw()
            sleep(1)
            turtle.update()

        self.selected_node = None
        for k in self.nodes.keys():
            self.nodes[k].selected = False

        if self.selected_node is not None:
            self.nodes[self.selected_node].selected = False
            self.selected_node = None
        if self.selected_edge is not None:
            self.edges[self.selected_edge].selected = False
            self.selected_edge = None

        for i in order[1]:
            self.selected_node = i
            self.nodes[self.selected_node].selected = True
            for k in self.edges.keys():
                self.edges[k].draw()
            for k in self.nodes.keys():
                self.nodes[k].draw()
            sleep(1)
            turtle.update()

        tur = self.turtle
        tur.ht()
        tur.pu()
        tur.goto(300, 20)
        tur.write(len(order[0]), font=("Arial", 10, "normal"))
        tur.goto(300, 0)
        tur.write("resuming program in 1 second", font=("Arial", 10, "normal"))
        sleep(1)

        self.selected_node = None
        for k in self.nodes.keys():
            self.nodes[k].selected = False

        turtle.onkeypress(self.bfs, 'b')
        turtle.onkeypress(self.draw, 'r')
        turtle.listen()
        self.busy = False
       
    # Piyush
    def dfs(self):
        self.busy = True
        try:
            starting_node = int(turtle.numinput("Starting node", "Enter Starting node: ", 0))
            to_find = int(turtle.numinput("End Node", "Which node to find", 0))
        except TypeError:
            self.busy = False
            return

        order = self.graph.DFS(starting_node, to_find)

        if self.selected_node is not None:
            self.nodes[self.selected_node].selected = False
            self.selected_node = None
        if self.selected_edge is not None:
            self.edges[self.selected_edge].selected = False
            self.selected_edge = None

        for i in order[0]:
            self.selected_node = i
            self.nodes[self.selected_node].selected = True
            for k in self.edges.keys():
                self.edges[k].draw()
            for k in self.nodes.keys():
                self.nodes[k].draw()
            sleep(1)
            turtle.update()

        self.selected_node = None
        for k in self.nodes.keys():
            self.nodes[k].selected = False

        if self.selected_node is not None:
            self.nodes[self.selected_node].selected = False
            self.selected_node = None
        if self.selected_edge is not None:
            self.edges[self.selected_edge].selected = False
            self.selected_edge = None

        for i in order[1]:
            self.selected_node = i
            self.nodes[self.selected_node].selected = True
            for k in self.edges.keys():
                self.edges[k].draw()
            for k in self.nodes.keys():
                self.nodes[k].draw()
            sleep(1)
            turtle.update()

        tur = self.turtle
        tur.ht()
        tur.pu()
        tur.goto(300, 20)
        tur.write(len(order[0]), font=("Arial", 10, "normal"))
        tur.goto(300, 0)
        tur.write("resuming program in 1 second", font=("Arial", 10, "normal"))

        self.selected_node = None
        for k in self.nodes.keys():
            self.nodes[k].selected = False

        turtle.onkeypress(self.dfs, 'x')
        turtle.onkeypress(self.draw, 'r')
        turtle.listen()
        self.busy = False
    #Shatakshi
    def getCoords(self):
        coords = {}
        for i in self.nodes:
            coords[i]=(self.nodes[i].x, self.nodes[i].y)
        return coords
    #Subhadip and Piyush
    def A_star(self):
        self.busy = True
        try:
            starting_node = int(turtle.numinput("Starting node", "Enter Starting node: ", 0))
            to_find = int(turtle.numinput("End Node", "Which node to find", 0))
            flag=int(turtle.numinput("Enter Preference For Heuristic Value Calculation", 
            "Enter 0 for Euclidean, and 1 for Manhattan: ", 0))
        except TypeError:
            self.busy = False
            return

        order = self.graph.aStarSearch(starting_node, to_find,self.getCoords(),flag)

        if self.selected_node is not None:
            self.nodes[self.selected_node].selected = False
            self.selected_node = None
        if self.selected_edge is not None:
            self.edges[self.selected_edge].selected = False
            self.selected_edge = None

        for i in order[0]:
            self.selected_node = i
            self.nodes[self.selected_node].selected = True
            for k in self.edges.keys():
                self.edges[k].draw()
            for k in self.nodes.keys():
                self.nodes[k].draw()
            sleep(1)
            turtle.update()

        self.selected_node = None
        for k in self.nodes.keys():
            self.nodes[k].selected = False

        if self.selected_node is not None:
            self.nodes[self.selected_node].selected = False
            self.selected_node = None
        if self.selected_edge is not None:
            self.edges[self.selected_edge].selected = False
            self.selected_edge = None

        for i in order[1]:
            self.selected_node = i
            self.nodes[self.selected_node].selected = True
            for k in self.edges.keys():
                self.edges[k].draw()
            for k in self.nodes.keys():
                self.nodes[k].draw()
            sleep(1)
            turtle.update()

        tur = self.turtle
        tur.ht()
        tur.pu()
        tur.goto(300, 20)
        tur.write(len(order[0]), font=("Arial", 10, "normal"))
        tur.goto(300, 0)
        tur.write("resuming program in 1 second", font=("Arial", 10, "normal"))

        self.selected_node = None
        for k in self.nodes.keys():
            self.nodes[k].selected = False

        turtle.onkeypress(self.A_star, 'a')
        turtle.onkeypress(self.draw, 'r')
        turtle.listen()
        self.busy = False
    
    #Piyush and Subhadip
    def AnimateShortestPath(self):
        self.busy = True
        try:
            starting_node = int(turtle.numinput("Starting node", "Enter Starting node: ", 0))
            to_find = int(turtle.numinput("End Node", "Which node to find", 0))
        except TypeError:
            self.busy = False
            return

        order = self.graph.FindShortestPath(starting_node, to_find)

        if self.selected_node is not None:
            self.nodes[self.selected_node].selected = False
            self.selected_node = None
        if self.selected_edge is not None:
            self.edges[self.selected_edge].selected = False
            self.selected_edge = None

        for i in order[0]:
            self.selected_node = i
            self.nodes[self.selected_node].selected = True
            for k in self.edges.keys():
                self.edges[k].draw()
            for k in self.nodes.keys():
                self.nodes[k].draw()
            sleep(1)
            turtle.update()

        self.selected_node = None
        for k in self.nodes.keys():
            self.nodes[k].selected = False

        if self.selected_node is not None:
            self.nodes[self.selected_node].selected = False
            self.selected_node = None
        if self.selected_edge is not None:
            self.edges[self.selected_edge].selected = False
            self.selected_edge = None

        for i in order[1]:
            self.selected_node = i
            self.nodes[self.selected_node].selected = True
            for k in self.edges.keys():
                self.edges[k].draw()
            for k in self.nodes.keys():
                self.nodes[k].draw()
            sleep(1)
            turtle.update()

        tur = self.turtle
        tur.ht()
        tur.pu()
        tur.goto(300, 20)
        tur.write(len(order[0]), font=("Arial", 10, "normal"))
        tur.goto(300, 0)
        tur.write("resuming program in 1 second", font=("Arial", 10, "normal"))

        self.selected_node = None
        for k in self.nodes.keys():
            self.nodes[k].selected = False

        turtle.onkeypress(self.bfs, 'j')
        turtle.onkeypress(self.draw, 'r')
        turtle.listen()
        self.busy = False

    def draw(self):
        try:
            if self.busy:
                return
            self.turtle.clear()
            turtle.update()
            self.stats.show_fps()
            turtle.ontimer(self.draw, 50)
        except Exception:
            print("Exiting...")
        for k in self.edges.keys():
            self.edges[k].draw()
        for k in self.nodes.keys():
            self.nodes[k].draw()
    
    # Chirag C     
    def excel(self):
        #path = r'C:\Users\alex\Desktop\file2.csv'
        path = turtle.textinput("Path for csv file", "Enter the path for the csv location")
        data=self.graph._graph    
        for i in range(len(data)):
            for j in range(len(data)):
                if j not in data[i].keys():
                    data[i][j]=-1
        pd.DataFrame(data).to_csv(path)
     
def main():
    turtle.tracer(0, 0)
    turtle.speed('fastest')
    turtle.mode("world")
    turtle.hideturtle()
    screen = turtle.getscreen()
    turtle.screensize(800, 800)
    screen.bgcolor("grey")

    gui = GraphGui(screen)
    turtle.onscreenclick(gui.on_left_click, 1, True)
    turtle.onkeypress(gui.bfs, 'b')
    turtle.onkeypress(gui.delete, 'd')
    turtle.onkeypress(gui.dfs, 'x')
    turtle.onkeypress(gui.excel, 't')
    turtle.onkeypress(gui.AnimateShortestPath,'j')
    turtle.onkeypress(gui.A_star,'a')
    screen.listen()
    screen.cv.unbind("<Motion>")
    gui.draw()

    turtle.mainloop()


main()
