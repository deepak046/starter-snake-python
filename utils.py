import numpy as np

def ManhDist(a, b):
    if type(a) and type(b) == list or type(a) and type(b) == tuple:
        return np.abs(a[0] - b[0]) + np.abs(a[1] - b[1])
    else:
        return np.abs(a.x - b.x) + np.abs(a.y - b.y)

def AstarDist(astar, a, b):
    path = astar.find_path(a, b)
    if path is not None:
      return len(path)
    else:
      return 100000

def getDirection(head, nextPos):
    if head["x"] == nextPos["x"]:
        if head["y"] > nextPos["y"]:
            return "down"
        else:
            return "up"
    else:
        if head["x"] > nextPos["x"]:
            return "left"
        else:
            return "right"