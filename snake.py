import numpy as np
import os

from flask import Flask
from flask import request

class Snake:
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.my_head = game_state["you"]["body"][0]
        self.my_neck = game_state["you"]["body"][1]

    '''
    Primary Functions 
    '''

    # Function to compute the minimax solution to the problem



    '''
    Helper Functions
    '''

    # Function to check safe moves
    # Function to compute the Astar distance between two points
