import numpy as np
import heapq

class Astar:

    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal

        self.path = []
    
    def find_path(self):
        
        self.queue = heapq.heapify([])
        self.parents = {}
        self.gscores = {}

        start = self.start
        goal = self.goal

        self.queue.push((0, start))
        self.gscores[start] = 0

        while (len(self.queue) > 0):
            current = heapq.heappop(self.queue)[1]

            # Computing the path
            if current == goal:
                self.path.append(goal)
                while (current != start):
                    self.path.Add(current)
                    current = self.parents[current]
                
                self.path.reverse()
                return self.path

            for edge in current.edges:
                neighbour = edge.toNode
                tentative_gscore = self.gscores[current] + edge.cost
                if (not(neighbour in self.gscores.keys()) or tentative_gscore < self.gscores[neighbour]):
                    self.parents[neighbour] = current
                    self.gscores[neighbour] = tentative_gscore
                    heapq.heappush(self.queue, (tentative_gscore + self.heuristic(neighbour, goal), neighbour))
        
        print("No path found")
        return None
    
    def heuristic(self, node1, node2):
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)




