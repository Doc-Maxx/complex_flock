import numpy as np

class space:
    def __init__(self, walls, connections):
        self.walls = walls
        self.connections = connections
        

class region:
    def __init__(self, type=='empty', origin==0+0j, eps == 0.0001)
        self.type = type
        self.origin = origin

class circle(region):
    def __init__(self, radius):
        self.radius = radius 

    def point_Within(self, point):
        return (point.real - origin.real)**2 + (point.imag - origin.imag)**2 < self.radius**2

    def vec_within(self, pos_vec):
        shifted_vec = pos_vec - origin
        return np.where(shift_vec<self.radius**2, True, False)

    def intersection(self, point, velocity):
        shifted_point = point - self.origin
        slope = - velocity.imag / (velocity.real + self.eps)
        c = shifted_point.real**2 + shifted_point.imag**2 - self.radius**2 - 2*shifted_point.real*shifted_point.imag*slope
        b = 2*slope*(-shifted_point.real*slope + shifted_point.imag)
        a = slope**2 + 1
        x_int = (-2*b + np.sqrt(b**2 - 4*a*c))/(2*a)
class rectangle(region):
    def __init__(self, point_2, thickness):
        self.thickness = thickness
        self.points = [origin, point_2]

    def point_Within(self, point):
        return 
    def vec_within:
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
