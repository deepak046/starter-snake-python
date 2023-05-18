import numpy as np
import os
import utils
import Astar
import graph
import time
import re #regex

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

        self.snakes = game_state["board"]["snakes"]

    '''
    Primary Functions 
    '''

    # Function to compute players to play out 
    def playOut(self, game_state, depth):
        '''
        game_state: current game state
        depth: depth of the search tree
        '''
        playersOut = []
        us = game_state["you"]

        # Check if head is within twice the search depth
        for snakes in game_state["board"]["snakes"]:
            if snakes["id"] != us["id"]:
                if utils.ManhDist(snakes["head"], us["head"])  <= 2*depth:
                    playersOut.append(snakes)
                else:
                    # Check if body is within the search depth 
                    for parts in snakes["body"]:
                        if utils.ManhDist(parts, us["head"]) <= depth:
                            playersOut.append(snakes)
                            break

        return playersOut
    
    # Function to mask the non-played out players
    def maskPlayers(self, game_state, playersOut, snakes):
        
        # Mask the players
        for snake in snakes:
            if snake in playersOut:
                snake["mask"] = 1
            else:
                snake["mask"] = 0

            if snake["friend"] == 1:
                snake["mask"] = 1
        
        return snakes
    
    def friends(self, game_state, snakes):
        
        for snake in snakes:
            txt = snake["name"]
            regList = re.findall("\ADD2438_G15.*", txt)
            if len(regList) > 0 and snake["id"] != game_state["you"]["id"]:
                snake["friend"] = 1
            else:
                snake["friend"] = 0
        
        return snakes
            
    
    # Function to implement the IDAPOS algorithm
    def IDAPOS(self, game_state, snakes, tCut):
        
        depth = 1
        alpha = -np.inf
        beta = np.inf

        start = time.time()
        tElapsed = 0

        while (tElapsed < tCut):
            
            playersOut = self.playOut(game_state, depth)
            friendSnakes = self.friends(game_state, snakes)
            maskSnakes = self.maskPlayers(game_state, playersOut, friendSnakes)

            if len(playersOut) == 2:
                bestMove = self.alphaBeta(game_state, maskSnakes, depth, alpha, beta, tCut)
            else:
                bestMove = self.maxN(game_state, maskSnakes, depth, alpha, beta, tCut)

            depth += 1
            tElapsed = time.time() - start

        return bestMove

    def children(self, game_state, currentSnake):

        children_states = []
        moves = []

        # for snake in game_state["board"]["snakes"]:
        #     if snake["id"] != currentSnake["id"]:
        for move in [(0,1), (0,-1), (-1,0), (1,0)]:
            # Append both next gamestate and the move leading up to that as a tuple and then add it to the list
            children_states.append((self.update_gamestate(game_state, move, currentSnake), move))

        return children_states, moves

    def update_gamestate(self, game_state, move, snake):

        # Find the snake index in the game state (done)
        # Check if the snake is "you" so that we have to update twice (done)
        # Reduce health if no food is eaten (done)
        # If next move is free, change the new head, new neck, new tail, new health and length of snake (done)
        # If next move has food, change the new head, new neck, and length of snake (done)
        # If next move is an obstacle, check if it's a wall or which snake it is.
            # If it's a wall, kill the snake and it's list (done)
            # If it's another snake or own snake body, once again kill it (done)
            # If it's a head of another snake, check if it's longer than you, if yes kill yourself, if not kill other snake (done)

        idx = game_state["board"]["snakes"].index(snake)
        boolYou = (snake["id"] == game_state["board"]["you"]["id"])
        # Next position of the head of the current snake
        temp_head_x = snake["head"]["x"] + move[0]
        temp_head_y = snake["head"]["y"] + move[1]  

        # Check if the next move for the head is valid    
        if self.graph.board[temp_head_x][temp_head_y] == 0:

            # Check if the next move doesn't have any food
            if [temp_head_x, temp_head_y] not in list(game_state["board"]["food"].values()):
                game_state["board"]["snakes"][idx]["head"]["x"] = temp_head_x
                game_state["board"]["snakes"][idx]["head"]["y"] = temp_head_y
                game_state["board"]["snakes"][idx]["neck"]["x"] = snake["head"]["x"]
                game_state["board"]["snakes"][idx]["neck"]["y"] = snake["head"]["y"]
                game_state["board"]["snakes"][idx]["body"].insert(0, {"x": temp_head_x, "y": temp_head_y})
                game_state["board"]["snakes"][idx]["body"].pop()
                game_state["board"]["snakes"][idx]["health"] -= 1

                if boolYou:
                    game_state["board"]["snakes"]["you"]["head"]["x"] = temp_head_x
                    game_state["board"]["snakes"]["you"]["head"]["y"] = temp_head_y
                    game_state["board"]["snakes"]["you"]["neck"]["x"] = snake["head"]["x"]
                    game_state["board"]["snakes"]["you"]["neck"]["y"] = snake["head"]["y"]
                    game_state["board"]["snakes"][idx]["body"].insert(0, {"x": temp_head_x, "y": temp_head_y})
                    game_state["board"]["snakes"][idx]["body"].pop()
                    game_state["board"]["snakes"]["you"]["health"] -= 1
            
            # Check if the next move has food
            else:
                game_state["board"]["snakes"][idx]["head"]["x"] = temp_head_x
                game_state["board"]["snakes"][idx]["head"]["y"] = temp_head_y
                game_state["board"]["snakes"][idx]["neck"]["x"] = snake["head"]["x"]
                game_state["board"]["snakes"][idx]["neck"]["y"] = snake["head"]["y"]
                game_state["board"]["snakes"][idx]["body"].insert(0, {"x": temp_head_x, "y": temp_head_y})
                game_state["board"]["snakes"][idx]["length"] += 1
                
                if boolYou:
                    game_state["board"]["snakes"]["you"]["head"]["x"] = temp_head_x
                    game_state["board"]["snakes"]["you"]["head"]["y"] = temp_head_y
                    game_state["board"]["snakes"]["you"]["neck"]["x"] = snake["head"]["x"]
                    game_state["board"]["snakes"]["you"]["neck"]["y"] = snake["head"]["y"]
                    game_state["board"]["snakes"][idx]["body"].insert(0, {"x": temp_head_x, "y": temp_head_y})              
                    game_state["board"]["snakes"][idx]["body"]["length"] += 1

        # If the next move is an obstacle
        else:

            # Check if the obstacle is a wall
            if temp_head_x < 0 or temp_head_x >= game_state["board"]["width"] or temp_head_y < 0 or temp_head_y >= game_state["board"]["height"]:
                game_state["board"]["snakes"].pop(idx)
                if boolYou:
                    game_state["board"]["snakes"]["you"].pop(idx)

            # Check if the obstacle is a snake
            else:
                for collideSnake in game_state["board"]["snakes"] and collideSnake["id"] != snake["id"]:
                    
                    if [temp_head_x, temp_head_y] == list(collideSnake["head"].values()):
                        
                        boolCollideYou = (collideSnake["id"] == game_state["board"]["you"]["id"])

                        # Check if the snake is longer, equal in length (or) shorter than you
                        if len(collideSnake["body"]) > len(snake["body"]): # Greater
                            game_state["board"]["snakes"].pop(idx)
                            if boolYou:
                                game_state["board"]["snakes"]["you"] = []

                        elif len(collideSnake["body"]) == len(snake["body"]): # Equal
                            game_state["board"]["snakes"].pop(idx)
                            collideidx = game_state["board"]["snakes"].index(collideSnake) # id of the snake we could head-on collide with
                            game_state["board"]["snakes"].pop(collideidx)
                            if boolYou:
                                game_state["board"]["snakes"]["you"] = []
                            elif boolCollideYou:
                                collideidx = game_state["board"]["snakes"].index(collideSnake) # id of the snake we could head-on collide with
                                game_state["board"]["snakes"]["you"] = []

                        else: # Smaller
                            collideidx = game_state["board"]["snakes"].index(collideSnake) # id of the snake we could head-on collide with
                            game_state["board"]["snakes"].pop(collideidx)
                            if boolCollideYou:
                                collideidx = game_state["board"]["snakes"].index(collideSnake) # id of the snake we could head-on collide with
                                game_state["board"]["snakes"]["you"] = []

                    # Check if the obstacle is a body of a snake
                    else:
                        if {"x":temp_head_x, "y":temp_head_y} in list(collideSnake["body"].values()):

                                game_state["board"]["snakes"].pop(idx)
                                if boolYou:
                                    game_state["board"]["snakes"]["you"] = []

        return game_state

    # Function to implement maxN algorithm
    def maxN(self, game_state, snakes, depth, maxPlayer, count=0):
        # Count and depth do the same job here (depth = 4 for 4 snakes and depth=8 for actual search depth of 2)
        
        snakeList = []
        # Get a list in the order [you, friend, enemy1, enemy2, ...]
        for snake in snakes:
            if snake["id"] != game_state["board"]["you"]["id"]:
                if snake["friends"] == 1:
                    snakeList.insert(0, snake)
                else:
                    snakeList.append(snake)
        
        snakeList.insert(0, game_state["board"]["you"])

        currentSnake = snakeList[count]

        if count >= 2:
            maxPlayer = False
        
        if depth == 0: # or self.isTerminal(game_state):
            return self.evaluateGame(game_state, game_state["board"]["you"], snakes)

        if snakes["mask"] == 1:
            
            if maxPlayer:
                maxEval = -np.inf

                for (childState, move) in self.children(game_state, currentSnake):
                    eval, _ = self.maxN(childState, snakes, depth-1, maxPlayer, count+1)
                    maxEval = max(maxEval, eval[count])
                    bestMove = move
                return maxEval, bestMove
            else:
                minEval = np.inf

                for (childState, move) in self.children(game_state, currentSnake):
                    eval, _ = self.maxN(childState, snakes, depth-1, maxPlayer, count+1)
                    minEval = min(minEval, eval[count])
                    bestMove = move
                return minEval, bestMove

    def alphaBeta(self, game_state, snakes, depth, alpha, beta, tCut):
        
        pass
        
        
    # Function to evaluate each game state
    def evaluateGame(self, game_state, snakeList):
        
        # Length advantage
        scoreVector = self.lengthScore(snakeList)

        # Snake health (number of turns until starvation >>>> distance to closest food)
        scoreVector += self.healthScore(snakeList)

        # Board control - Voronoi diagrams
        scoreVector += self.areaScore(game_state, snakeList)

        return scoreVector       

    # # Function to evaluate leaf nodes

    def lengthScore(self, snakeList):

        lenScore = []
        
        lengthVec = []
        for snake in snakeList:
            lengthVec.append(snake["length"])
        
        # sortIndex = np.argsort(np.array(lengthVec))

        maxLen = max(lengthVec)
        maxMask = lengthVec[lengthVec == maxLen]

        sumList = np.sum(np.array(maxMask))

        for idx, snake in enumerate(snakeList):
            if maxMask[idx] == 1 and sumList == 1:
                lenScore.append(1.5)
            elif maxMask[idx] == 1 and sumList > 1:
                lenScore.append(0.5)
            else:
                lenScore.append(0)
        
        return lenScore
    
    def healthScore(self, snakeList):

        healthVec = []

        for snake in snakeList:
            healthVec.append(snake["health"] - utils.ManhDist(list(snake["head"].values()), self.closestFood()))

        return healthVec     
        

    def areaScore(self, game_state, snakeList):

        areaScore = np.zeros((game_state["board"]["width"], game_state["board"]["height"]))
        areaVec = 5*np.ones(len(snakeList))/(game_state["board"]["width"]*game_state["board"]["height"])

        for x in range(game_state["board"]["width"]):
            for y in range(game_state["board"]["height"]):
                min = np.inf
                for idx, snake in enumerate(snakeList):
                    if utils.ManhDist([x,y], list(snake["head"].values())) < min:
                        min = utils.ManhDist([x,y], list(snake["head"].values()))
                        areaScore[x][y] = idx
        
        for idx, snake in enumerate(snakeList):
            areaVec[idx] = areaVec[idx]*(np.sum(areaScore[areaScore == idx]))

        return areaVec   

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
