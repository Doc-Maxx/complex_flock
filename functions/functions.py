import numpy as np

class space:
    def __init__(self, walls, connections):
        self.walls = walls
        self.connections = connections

class wall:
    def __init__(self, point_1, point_2, thickness):
        self.points = [point_1, point_2]
        self.thickness = thickness
        self.diff = point_2 - point_1
        self.slope = np.imag(self.diff) / np.real(self.diff)
        self.y_intercept = np.imag(point_1) - self.slope*np.real(point_1)
        self.x_intercept = np.imag(point_1) / self.slope - np.real(point_1)
        self.shift = self.shift_comp
        self.ori = self.diff * 1j
    
    def shift_comp(self):
        if self.y_intercept < self.x_intercept:
            return 0 + self.y_intercept * 1j
        else:   
            return self.x_intercept + 0j
