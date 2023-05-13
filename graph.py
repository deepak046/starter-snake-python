import numpy as np
import os

class Edge:

    def __init__(self, fromNode, toNode, cost):
        self.fromNode = fromNode
        self.toNode = toNode
        self.cost = cost

class Node:

    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.edges = []

class Graph:

    def __init__(self, game_state):
        self.game_state = game_state
        self.board = game_state["board"]

        self.width = self.board["width"]
        self.height = self.board["height"]

        self.hazards = self.board["hazards"]
        self.snakes = self.board["snakes"]

        self.you = game_state["you"]

        # Get the current board with free spaces and obstacles
        self.boardGraph = self.get_board()
    
    def get_obstacles(self):

        obstacles = []

        # Add all snake bodies to obstacles (including heads)
        for snake in self.snakes:
            for body in snake["body"]:
                obstacles.append(body)

        # Add all hazards to obstacles
        for hazard in self.hazards:
            obstacles.append(hazard)

        return obstacles

    def get_board(self):
        
        NodeArray = []

        for x in range(self.width):
            for y in range(self.height):

                if (x,y) not in self.get_obstacles():
                    node = Node(x, y)

                    # Add edges to node from all 4 directions if not an obstacle or wall
                    
                    if x > 0 and (x-1, y) not in self.get_obstacles():
                        left = Node(x-1, y)
                        node.edges.append(Edge(node, left, 1))
                        left.edges.append(Edge(left, node, 1))
                    elif x < self.width - 1 and (x+1, y) not in self.get_obstacles():
                        right = Node(x+1, y)
                        node.edges.append(Edge(node, right, 1))
                        right.edges.append(Edge(right, node, 1))
                    elif y > 0 and (x, y-1) not in self.get_obstacles():
                        down = Node(x, y-1)
                        node.edges.append(Edge(node, down, 1))
                        down.edges.append(Edge(down, node, 1))
                    elif y < self.height - 1 and (x, y+1) not in self.get_obstacles():
                        up = Node(x, y+1)
                        node.edges.append(Edge(node, up, 1))
                        up.edges.append(Edge(up, node, 1))

                    NodeArray.append(node)


        return NodeArray
    
