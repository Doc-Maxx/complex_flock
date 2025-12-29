import numpy as np

class space:
    def __init__(self, walls, connections):
        self.walls = walls
        self.connections = connections

class wall:
    def __init__(self, point_1, point_2,thickness):
        self.points = [point_1, point_2]
        self.thickness = thickness
        self.ori = 
        self.diff = point_2 - point_1
        self.slope = np.imag(self.diff) / np.real(self.diff)
        
