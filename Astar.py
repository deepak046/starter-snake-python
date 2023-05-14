import numpy as np
import heapq
import typing
import utils
from graph import Graph, Node

from queue import PriorityQueue
    
class Astar:

    def __init__(self, graph):
        self.graph = graph
    
    def find_path(self, start, goal):
        # print("board: ", self.graph.board)
        path = []    
      
        # Initializing priority queue
        queue = PriorityQueue()
        gscores = {}
        parents = {}

        # Initializing start and end tuples
        start = (start["x"], start["y"])
        goal = (goal["x"], goal["y"])

        # Adding the start pos to the PQueue
        queue.put(start, 0)
        gscores[start] = 0

        while not queue.empty():
            current = queue.get()
            # print("Current: ", current)
            # print("queue size: " , queue.qsize())
          
            # Computing the final path
            if current == goal:
                # path.append(goal)
                while (current != start):
                    path.append(current)
                    current = parents[current]
                
                path.reverse()
                # print("path: ", path)
                print("path found from ", start, " to ", goal)
                return path

            # Iterating over all the edges (East, South, West, North)
          
            # print("================")
            # print("Current: ", current)
          
            for d in "ESWN":
                if d == "E":
                    neighbour = (current[0] + 1, current[1])
                elif d == "S":
                    neighbour = (current[0], current[1] - 1)
                elif d == "W":
                    neighbour = (current[0] - 1, current[1])
                elif d == "N":
                    neighbour = (current[0], current[1] + 1)
                  
                # print("neighbor: ", neighbour)
              

                # Checking if the neighbour grid is valid (continue if not)
                if (neighbour[0] < 0 or neighbour[0] >= self.graph.width or neighbour[1] < 0 or neighbour[1] >= self.graph.height or self.graph.board[neighbour[0]][neighbour[1]] == 1):
                    continue

                temp_gscore = gscores[current] + 1
                if (not(neighbour in gscores.keys()) or temp_gscore < gscores[neighbour]):
                    parents[neighbour] = current
                    gscores[neighbour] = temp_gscore
                    queue.put(neighbour, temp_gscore + self.heuristic(neighbour, goal))
        
        print("No path found from ", start, " to ", goal)
        return None
    
    def heuristic(self, node1, node2):
        return utils.ManhDist(node1, node2)




