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

    def intersection(self): # if a position(s) is within the circle we can compute where it intersected the boundary given a velocity
        shifted_point = self.list_pos - self.origin # shift the point(s) to work around the origin
        slope = - self.list_vel.imag / (self.list_vel.real + self.eps) # compute the slope of the line defining the trajectory from the last point
        # The algebra results in a quadratic equation - what follows is a calculation for a b and c
        # To do this self solve the system of equations for defining a circle and a line
        c = shifted_point.real**2 + shifted_point.imag**2 - self.radius**2 - 2*shifted_point.real*shifted_point.imag*slope
        b = 2*slope*(-shifted_point.real*slope + shifted_point.imag)
        a = slope**2 + 1
        # We take the positive solution
        x_int = (-2*b + np.sqrt(b**2 - 4*a*c))/(2*a)
        y_int = slope*x_int + shifted_point.imag - slope*shifted_point.real
        intersection_point = x_int + y_int*1j
        return intersection_point # return the intersection point as a complex value

    def push(self): # using the intersection_point method, this computes the new position and velocity for the region list
        # that is it enforces the boundary by pushing flockers out of the (semi)circle
        # returns nothing
        diff = self.list_pos-self.intersection_point # find the number between the intersection point and the point within
        self.list_pos = self.intersection_point-diff*1j # move perpendicularly that distance from UHHH NEED TO CHECK THIS MATH
        reflected_angle = np.angle(self.intersection_point)-np.angle(self.list_vel)+np.pi
        self.list_vel = self.list_vel * np.e**(-1j * reflected_angle)
  
class rectangle(region):
    def __init__(self, origin, point_2, thickness, eps = 0.0001):   
        self.eps = eps # used to compute the slope to avoid infinities
        self.origin = origin # sort of the lower left corner of a rectangle. The rectangle is created by drawing from here to Point_2 
        self.thickness = thickness # distance we extrude the rectangle into the i-direction.
        self.diff = point_2 - origin # shifts point 2 to the origin
        self.angle = np.angle(self.diff) 
        self.extrusion = self.thickness * (self.diff / abs(self.diff)) * 1j # creates a number rotated by i to extrude the rectangle by
        self.points = np.array([origin, point_2, origin + self.extrusion, point_2 + self.extrusion]) # all four points
        self.slope = self.diff.imag / (self.diff.real + self.eps) # slope of the line defined by the origin and point_2
        self.rotated_points = self.points * np.e**(-1j * self.angle) # all four points rotated such that the origin and point_2 have zero slope

    def rotate_points(self, points, u = 1): # rotates points as much as the rectangle needs to be rotated for self.rotate_points
        return points * np.e**(-1j * self.angle * u)

    def point_Within(self, point): # checks if a point lies within the rectanglular region
        # We first rotate the point and the check to see if it falls within the rotated rectangle
        # returns a boolean
        point_check = self.rotate_points(point)
        hori_check = self.rotated_points[0].real < point_check.real < self.rotated_points[1].real
        vert_check = self.rotated_points[0].imag < point_check.imag < self.rotated_points[2].imag
        return hori_check and vert_check

    def vec_within(self, pos_vec): # checks if a vector of points fall within a rectangle region
        # First we rotate the points and then check to see if they fall within the rotated rectangle
        # returns a vector of booleans
        rotate_vec = rotate_points(pos_vec)
        return np.where(    
                        self.rotated_points[0].real < rotate_vec.real < self.rotated_points[1].real
                        and self.rotated_points[0].imag < rotate_vec.imag < self.rotated_points[1].imag,
                        True, False
                        )

    def push(self): # pushes flockers out of the rectangle as if the line between the origin and point_2 were a reflecting wall
        # returns nothing
        shifted_point = self.list_pos - self.origin # shift the to the origin
        shifted_point = self.rotate_points(shifted_point) # rotate the points to align with the rotated rectangle 
        shifted_point = np.conjugate(shifted_point) # conjugate the number to reflect the position across the diff line
        shifted_point = self.rotate_points(shifted_point, u = -1) # rotate the points back
        self.list_pos = shifted_point + self.origin # undo the origin shift to find the new true positions

        rotated_vel = self.rotate_points(self.list_vel) # rotate the velocities as well they do no need to shifted
        rotated_vel = np.conjugate(rotated_vel) # reflect the verticle velocity component
        self.list_vel = self.rotate_points(rotated_vel, u=-1) # undo the rotation and set the new velocities
        
class manifest:
    def __init__(self):
        self.pos_master = np.array([]) # master list of positions 
        self.vel_master = np.array([]) # master list of velocities

    def step(self, space): # steps the manifest forward one time step
        self.pos_master = self.pos_master + self.vel_master*space.dt

    def add_flocker(self, pos, vel): # adds a flocker to the list
        self.pos_master=np.append(self.pos, pos)
        self.vel_master=np.append(self.vel, vel)

    def spawn_flockers(self, N, region, alignment='random'): # generates a list of flockers 
        # this is done within around the origin of a region
        positions=np.random.rand(N,2).view(np.complex128).flatten()+region.origin
        velocities=np.random.rand(N,2).view(np.complex128).flatten()
        self.pos_master=np.append(self.pos_master, positions)
        self.vel_master=np.append(self.vel_master, velocities)

    def split_flockers(self, regions): # This splits the manifest by filling each region with flockers within each region
        for i in regions:
            condition_split = i.vec_within(self.pos_master)
            i.list_pos = np.extract(condition_split, self.pos_master)
            i.list_vel = np.extract(condition_split, self.vel_master)

    def enforce_boundary(self, regions):
        for i in regions:
            conidtion = i.vec_within(self.i.list_pos)

  
