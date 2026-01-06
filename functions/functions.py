import numpy as np

class space:
    def __init__(self, regions, manifest,):
        self.regions = regions # list of regions, contains geometric information inparticular boundaries
        self.manifest = manifest # list of flockers
        self.dt = dt # step size

class region:
    def __init__(self, origin=0+0j, eps = 0.0001):
        self.type = "" # regions are (semi)circles and rectangles, they automatically assign their type themselves
        self.origin = origin # origin point, each region shape is built around this point
        self.eps = eps # small value to avoid infinite slops in special intersection cases
        self.list_pos = np.array([]) # Each region can have a list of flockers assigned to it via the manifest
        self.list_vel = np.array([]) # same but contains their velocity information

class circle(region):
    def __init__(self, origin,radius,arc=np.array([-np.pi, np.pi]), eps = 0.0001):
        self.origin = origin # center of the circle or semicircle
        self.radius = radius 
        self.type = "circle" 
        self.eps = eps
        self.arc = arc #defines angle for the semicircle default is a whole circle. The first value is the clockwise swing from the horizontal and the second is the counter clockwise

    def point_Within(self, point): # Checks if a single point is within the the (semi)circle
        # It first shifts the point relative to the origin of the circle
        # then checks the argument and mangnitude of the complex number fall within the radius and semicircle arc
        # Returns a boolean
        angle = np.angle(point)
        return (point.real - origin.real)**2 + (point.imag - origin.imag)**2 < self.radius**2 and self.arc[0]<=angle<self.arc[1]
    
    def vec_within(self, pos_vec): # checks if a vector of positions fall within the region
        # returns a vector of booleans 
        # shift all the positions to be around the origin
        shifted_vec = pos_vec - self.origin
        angle = np.angle(shifted_vec) # compute angles for all the shifted vectors. This has to be done after the origin shift.
        # next we build alist of conditions to play nicely with booleans and vectors and conditions
        c1 = np.absolute(shifted_vec)<self.radius # first we check that we are within the raidus
        c2 = angle < self.arc[1] # second we check we are below the counter-clockwise sweeping angle
        c3 = self.arc[0] <= angle # third we check we are above or ar the clockwise sweeping angle
        condition = np.all([c1,c2,c3],axis=0) # Using np.all we create a combined condition, logically identical to "and" statements
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

    def rotate_points(self, points, u = 1):
        return points * np.e**(-1j * self.angle * u)

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

    def push(self):
        shifted_point = self.list_pos - self.origin
        shifted_point = self.rotate_points(shifted_point)
        shifted_point = np.conjugate(shifted_point)
        shifted_point = self.rotate_points(shifted_point, u = -1)
        self.list_pos = shifted_point + self.origin

        rotated_vel = self.rotate_points(self.list_vel)
        rotated_vel = np.conjugate(rotated_vel)
        self.list_vel = self.rotate_points(rotated_vel, u=-1)



        
class manifest:
    def __init__(self):
        self.pos_master = np.array([])
        self.vel_master = np.array([])

    def step(self, space):
        self.pos_master = self.pos_master + self.vel_master*space.dt

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


