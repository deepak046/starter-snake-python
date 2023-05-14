import numpy as np
import os
import utils
import Astar
import graph

class Snake:
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.my_head = game_state["you"]["body"][0]
        self.my_neck = game_state["you"]["body"][1]
        self.my_tail = game_state["you"]["body"][-1]
        self.my_before_tail = game_state["you"]["body"][-2]

        self.graph = graph.Graph(game_state)
        self.astar = Astar.Astar(self.graph)

        self.food = game_state["board"]["food"]

    '''
    Primary Functions 
    '''

    # # Function to compute players to play out 
    # def playOut(game_state, depth):
    #     '''
    #     game_state: current game state
    #     depth: depth of the search tree
    #     '''
    #     playersOut = []
    #     us = game_state["you"]

    #     # Check if head is within twice the search depth
    #     for snakes in game_state["board"]["snakes"]:
    #         if snakes["id"] != us["id"]:
    #             if utils.ManhDist(snakes["head"], us["head"])  <= 2*depth:
    #                 playersOut.append(snakes)
    #             else:
    #                 # Check if body is within the search depth 
    #                 for parts in snakes["body"]:
    #                     if utils.ManhDist(parts, us["head"]) <= depth:
    #                         playersOut.append(snakes)
    #                         break

    #     return playersOut
    
    def closestFood(self):

        foods = self.food

        closest = foods[0]
        closestDist = 10000000
        path = self.astar.find_path(self.my_head, closest)
        if path is not None:
          closestDist = len(path)
          nextPos = {"x":path[0][0], "y":path[0][1]}

        for food in foods:
            if utils.AstarDist(self.astar, food, self.my_head) < closestDist:
                closest = food
                path = self.astar.find_path(self.my_head, closest)
                if path is not None:
                  closestDist = len(path)
                  nextPos = {"x":path[0][0], "y":path[0][1]}

        if path is None:
          # no path to a food found, go to end of tail
          dx = self.my_before_tail[0] - self.my_tail[0]
          dy = self.my_before_tail[1] - self.my_tail[1]
          end = [self.my_tail[0]+dx, self.my_tail[1]]
          path = self.astar.find_path(self.my_head, self.my_tail) 
          if path is None: 
            nextPos = {"x":0,"y":0}
            print("we are doomed")
          else:
            nextPos = {"x":path[0][0], "y":path[0][1]}
          
                        
        print("current path: ", path)
        return closest, nextPos
    






    
    '''
    Helper Functions
    '''

    # Function to check safe moves
    # Function to compute the Astar distance between two points
