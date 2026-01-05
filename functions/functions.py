import numpy as np

class space:
    def __init__(self, regions, manifest):
        self.regions = regions
        self.manifest = manifest

class region:
    def __init__(self, origin=0+0j, eps = 0.0001):
        self.type = ""
        self.origin = origin
        self.eps = eps
        self.list_pos = np.array([])
        self.list_vel = np.array([])

class circle(region):
    def __init__(self, origin,radius,arc=np.array([-np.pi, np.pi]), eps = 0.0001):
        self.origin = origin
        self.radius = radius 
        self.type = "circle"
        self.eps = eps
        self.arc = arc

    def point_Within(self, point):
        angle = np.angle(point)
        return (point.real - origin.real)**2 + (point.imag - origin.imag)**2 < self.radius**2 and self.arc[0]<angle<self.arc[1]
    
    def vec_within(self, pos_vec):
        shifted_vec = pos_vec - self.origin
        angle = np.angle(shifted_vec)
        c1 = np.absolute(shifted_vec)<self.radius
        c2 = angle < self.arc[1]
        c3 = self.arc[0] <= angle
        condition = np.all([c1,c2,c3],axis=0)
        return np.where(condition,True, False)

    def intersection(self):
        shifted_point = self.list_pos - self.origin
        slope = - self.list_vel.imag / (self.list_vel.real + self.eps)
        c = shifted_point.real**2 + shifted_point.imag**2 - self.radius**2 - 2*shifted_point.real*shifted_point.imag*slope
        b = 2*slope*(-shifted_point.real*slope + shifted_point.imag)
        a = slope**2 + 1
        x_int = (-2*b + np.sqrt(b**2 - 4*a*c))/(2*a)
        y_int = slope*x_int + shifted_point.imag - slope*shifted_point.real
        intersection_point = x_int + y_int*1j
        return intersection_point

    def push(self):
        diff = self.list_pos-self.intersection_point
        self.list_pos = self.intersection_point-diff*1j
        reflected_angle = np.angle(self.intersection_point)-np.angle(self.list_vel)+np.pi
        self.list_vel = self.list_vel * np.e**(-1j * reflected_angle)
  
class rectangle(region):
    def __init__(self, origin, point_2, thickness, eps = 0.0001):   
        self.eps = eps
        self.origin = origin
        self.thickness = thickness
        self.diff = point_2 - origin
        self.angle = np.angle(self.diff)
        self.extrusion = self.thickness * (self.diff / abs(self.diff)) * 1j
        self.points = np.array([origin, point_2, origin + self.extrusion, point_2 + self.extrusion])
        self.slope = self.diff.imag / (self.diff.real + self.eps)
        self.rotated_points = self.points * np.e**(-1j * self.angle) 

    def rotate_points(self, points):
        return points * np.e**(-1j * self.angle)

    def point_Within(self, point):
        point_check = self.rotate_points(point)
        hori_check = self.rotated_points[0].real < point_check.real < self.rotated_points[1].real
        vert_check = self.rotated_points[0].imag < point_check.imag < self.rotated_points[2].imag
        return hori_check and vert_check

    def vec_within(self, pos_vec):
        rotate_vec = rotate_points(pos_vec)
        return np.where(    
                        self.rotated_points[0].real < rotate_vec.real < self.rotated_points[1].real
                        and self.rotated_points[0].imag < rotate_vec.imag < self.rotated_points[1].imag,
                        True, False
                        )
        
class manifest:
    def __init__(self):
        self.pos_master = np.array([])
        self.vel_master = np.array([])

    def spawn_flockers(self, N, region, alignment='random'):
        positions=np.random.rand(N,2).view(np.complex128).flatten()+region.origin
        velocities=np.random.rand(N,2).view(np.complex128).flatten()
        self.pos_master=np.append(self.pos_master, positions)
        self.vel_master=np.append(self.vel_master, velocities)

    def split_flockers(self, regions):
        for i in regions:
            condition_split = i.vec_within(self.pos_master)
            i.list_pos = np.extract(condition_split, self.pos_master)
            i.list_vel = np.extract(condition_split, self.vel_master)

    def enforce_boundary(self, regions):
        for i in regions:
            conidtion = i.vec_within(self.i.list_pos)


