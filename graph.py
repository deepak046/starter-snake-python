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

        # Width and height of the board
        self.width = self.board["width"]
        self.height = self.board["height"]

        # List of all battlesnake objects
        self.snakes = self.board["snakes"]

        # Battlesnake object with all the info about our snake
        self.you = game_state["you"]

        # Get the current board with free spaces and obstacles
        self.board = self.get_board()
    
    def get_obstacles(self):

        obstacles = []
        count = 0
        # Add all snake bodies to obstacles (including heads)
        for snake in self.snakes:
            for body in snake["body"]:
                obstacles.append((body["x"], body["y"]))
                count += 1
        # print("Number of obstacles: {}".format(count))

        return obstacles

    def get_board(self):
        
        NodeArray = []

        # Assign 1 for every grid with and obstacle and 0 for free (creates a 2D array)
        for x in range(self.width):
            nodeRow = []
            for y in range(self.height):
                if (x,y) in self.get_obstacles():
                    nodeRow.append(1)
                else:
                    nodeRow.append(0)
            NodeArray.append(nodeRow)

        return NodeArray
    
