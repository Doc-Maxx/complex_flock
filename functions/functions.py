import numpy as np
import scipy.spatial as spp
import copy
from copy import deepcopy

class space:
    def __init__(self, regions, manifest, dt):
        self.regions = regions # list of regions, contains geometric information inparticular boundaries
        self.container_regions = self.create_container_regions()
        self.boundary_regions = self.create_boundary_regions()
        self.manifest = manifest # list of flockers
        self.dt = dt # step size
        

    def create_container_regions(self):
        container_regions = []
        for i in self.regions:
            if i.boundary == False:
                container_regions.append(i)
        return container_regions

    def create_boundary_regions(self):
        b_regions = []
        for i in self.regions:
            if i.boundary == True:
                b_regions.append(i)
        return b_regions

class region:
    def __init__(self, origin=0+0j, eps = 0.0001, boundary_bool=False):
        self.type = "" # regions are (semi)circles and rectangles, they automatically assign their type themselves
        self.origin = origin # origin point, each region shape is built around this point
        self.eps = eps # small value to avoid infinite slops in special intersection cases
        self.list_pos = np.array([]) # Each region can have a list of flockers assigned to it via the manifest
        self.list_vel = np.array([]) # same but contains their velocity information
        self.boundary = boundary_bool # boolean to indicate a regions status as a boundary 
        
class ring(region):
    def __init__(self, origin, radius_inner, radius_outer, arc=np.array([-np.pi,np.pi]),boundary_bool=False):
        region.__init__(self, origin=origin, eps=0.0001,boundary_bool=boundary_bool)
        self.type="ring"
        self.radius_inner=radius_inner
        self.radius_outer=radius_outer
        self.arc = arc

    def vec_within(self, pos_vec): # checks if a vector of points fall withihn a ring
        # returns a vector of booleans
        shifted_vec = pos_vec - self.origin # shift to the origin
        mags = np.absolute(shifted_vec) # precompute magnitudes
        ang = np.angle(shifted_vec) # precompute arguments
        c1 = mags <= self.radius_outer 
        c2 = self.radius_inner <= mags
        c3 = ang < self.arc[1]  
        c4 = self.arc[0] <= ang
        condition = np.all([c1,c2,c3,c4],axis=0)
        return np.where(condition, True, False)

    def intersection(self):
        shifted_point = self.list_pos - self.origin # shift the point(s) to work around the origin
        slope = - self.list_vel.imag / (self.list_vel.real + self.eps) # compute the slope of the line defining the trajectory from the last point
        # The algebra results in a quadratic equation - what follows is a calculation for a b and c
        # To do this self solve the system of equations for defining a circle and a line
        c = shifted_point.real**2 + shifted_point.imag**2 - self.radius_inner**2 - 2*shifted_point.real*shifted_point.imag*slope
        b = 2*slope*(-shifted_point.real*slope + shifted_point.imag)
        a = slope**2 + 1
        # We take the positive solution
        x_int = (-2*b + np.sqrt(b**2 - 4*a*c))/(2*a)
        y_int = slope*x_int + shifted_point.imag - slope*shifted_point.real
        intersection_point = x_int + y_int*1j
        return intersection_point # return the intersection point as a complex value

    def rotate_points(self, angle, points, u = 1): # rotates points such that they lie entirely on the imaginary axis
        return points * np.e**(-1j * (angle - np.pi) * u ) # this method works differently than the other rotare points

    def push(self): # pushes boids out into the interior side of th:withihne ring
        # returns nothing 
        # We rotate the points counter clockwise so that their corresponding intersection points lie on the imaginary axis
        # We then reflect the velocity and positions across the horizontal line intersecting that intersection point
        # This reflection is done by taking the complex conjugate
        intersection_angles = np.angle(self.intersection())
        shifted_point = self.list_pos - self.origin
        shifted_point = self.rotate_points(intersection_angles, shifted_point)
        shifted_point = np.conjugate(shifted_point)
        self.list_pos = self.rotate_points(intersection_angles, shifted_point, u=-1) + self.origin

        shifted_vel = self.rotate_points(intersection_angles, self.list_vel)
        shifted_vel = np.conjugate(shifted_vel)
        self.list_vel = self.rotate_points(intersection_angles, shifted_vel, u=-1)

class circle(region):
    def __init__(self, origin,radius,arc=np.array([-np.pi, np.pi]), eps = 0.0001, boundary_bool=False):
        self.origin = origin # center of the circle or semicircle
        self.radius = radius 
        self.type = "circle" 
        self.eps = eps
        self.arc = arc #defines angle for the semicircle default is a whole circle. The first value is the clockwise swing from the horizontal and the second is the counter clockwise
        self.boundary = boundary_bool
        self.list_pos = np.array([]) # Each region can have a list of flockers assigned to it via the manifest
        self.list_vel = np.array([]) # same but contains their velocity information

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
        diff = self.list_pos-self.intersection() # find the number between the intersection point and the point within
        self.list_pos = self.intersection()-diff*1j # move perpendicularly that distance from UHHH NEED TO CHECK THIS MATH
        reflected_angle = np.angle(self.intersection())-np.angle(self.list_vel)+np.pi
        self.list_vel = self.list_vel * np.e**(-1j * reflected_angle)
  
class rectangle(region):
    def __init__(self, origin, point_2, thickness, eps = 0.0001,boundary_bool=False):   
        self.eps = eps # used to compute the slope to avoid infinities
        self.origin = origin # sort of the lower left corner of a rectangle. The rectangle is created by drawing from here to Point_2 
        self.thickness = thickness # distance we extrude the rectangle into the i-direction.
        self.diff = point_2 - origin # shifts point 2 to the origin
        self.angle = np.angle(self.diff) 
        self.extrusion = self.thickness * (self.diff / abs(self.diff)) * 1j # creates a number rotated by i to extrude the rectangle by
        self.points = np.array([origin, point_2, origin + self.extrusion, point_2 + self.extrusion]) # all four points
        self.slope = self.diff.imag / (self.diff.real + self.eps) # slope of the line defined by the origin and point_2
        self.rotated_points = self.points * np.e**(-1j * self.angle) # all four points rotated such that the origin and point_2 have zero slope
        self.boundary = boundary_bool
        self.list_pos = np.array([]) # Each region can have a list of flockers assigned to it via the manifest
        self.list_vel = np.array([]) # same but contains their velocity information
        self.type = "rectangle"

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
        rotate_vec = self.rotate_points(pos_vec)
        
        c1 = self.rotated_points[0].real <= rotate_vec.real 
        c2 = rotate_vec.real <= self.rotated_points[1].real 
        c3 = self.rotated_points[0].imag <= rotate_vec.imag
        c4 = rotate_vec.imag <= self.rotated_points[2].imag

        condition = np.all([c1,c2,c3,c4],axis=0)
        return np.where( condition, True, False )

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
    def __init__(self, radius, velocity_scale):
        self.pos_master = np.array([]) # master list of positions 
        self.vel_master = np.array([]) # master list of velocities
        self.velocity_scale = velocity_scale
        self.radius = radius


    def step(self, space): # steps the manifest forward one time step
        self.pos_master = self.pos_master + self.vel_master*space.dt

    def add_flocker(self, pos, vel): # adds a flocker to the list
        # returns nothing
        self.pos_master=np.append(self.pos_master, pos)
        self.vel_master=np.append(self.vel_master, vel)

    def spawn_flockers(self, N, region, alignment='random'): # generates a list of flockers 
        if region.type != "rectangle":
            print("spawn_flockers only supports rectangular regions.")
        else:
            # this is done within around the origin of a region
            positions=np.random.rand(N,2).view(np.complex128).flatten()
            velocities=np.random.rand(N,2).view(np.complex128).flatten()*self.velocity_scale
            #need to scale the flockers and rotate them by rectangle region's angle
            pos_real = np.real(positions)*np.abs(region.diff)
            pos_imag = np.imag(positions)*region.thickness
            positions = pos_real + pos_imag*1j
            positions = region.rotate_points(positions, u=-1) + region.origin
  
            self.pos_master=np.append(self.pos_master, positions)
            self.vel_master=np.append(self.vel_master, velocities)

    def split_flockers(self, space): # This splits the manifest by filling each region with flockers within each region
        # returns nothing
        # This method allows overlapping regions to have duplicate flockers
        for i in space.regions: # loop through region list 
            condition_split = i.vec_within(self.pos_master) # create boolean conditions for splitting up the master list into regional lists 
            i.list_pos = np.extract(condition_split, self.pos_master)
            i.list_vel = np.extract(condition_split, self.vel_master)

    def reform_master_list(self, space):
        v = np.array([])
        p = np.array([])
        for i in space.container_regions:
            v = np.append(v, i.list_vel)
            p = np.append(p, i.list_pos)
        self.vel_master = v
        self.pos_master = p

    def enforce_boundary(self, regions): # this loops through the regions and pushes out flockers that are within boundary regions
        for i in regions:
            if i.boundary == True:
                i.push()
                for j in regions:
                    condition = j.vec_within(i.list_pos)
                    to_remove_pos = np.extract(condition, i.list_pos)
                    to_remove_vel = np.extract(condition, i.list_vel)
                    j.list_pos = np.append(j.list_pos, to_remove_pos)
                    j.list_vel = np.append(j.list_vel, to_remove_vel)
                    i.list_pos = i.list_pos[np.invert(condition)]
                    i.list_vel = i.list_vel[np.invert(condition)]




    def update_velocity(self, space):
        space_copy = copy.deepcopy(space) # Make a deep copy of the space it will fix the ordering issue
        for i in range(len(space.container_regions)):
            pos, vel, slices = self.connect_adj_regions(space_copy, i)
            tree = self.make_tree(pos) 
            for j in range(len(space.container_regions[i].list_pos)):
                pos_local = space.container_regions[i].list_pos
                pos_local = np.array([np.real(pos_local), np.imag(pos_local)])
                hood = self.get_hood(pos_local[:,j],tree)
                space.container_regions[i].list_vel[j] = np.average(vel[hood])
               
        self.reform_master_list(space)

    def connect_adj_regions(self, space, index): # creats a shared list between adjacent regions
        # returns list of velocities and positions of all flockers contained in adjacent and the region of interest
        # this function assumes regions in the regions list are adjacent, so whe using it use care to arrange regions that way
        n_pos_list= np.array([])
        n_vel_list= np.array([])
        i = index
        region = space.container_regions
                                          
        n_pos_list = np.append(n_pos_list, region[i].list_pos)
        n_pos_list = np.append(n_pos_list, region[i-1].list_pos)
        n_pos_list = np.append(n_pos_list, region[(i+1)%len(region)].list_pos)
        
        n_vel_list = np.append(n_vel_list, region[i].list_vel)
        n_vel_list = np.append(n_vel_list, region[i-1].list_vel)
        n_vel_list = np.append(n_vel_list, region[(i+1)%len(region)].list_vel)

        return n_pos_list, n_vel_list,  [len(region[i-1].list_pos),len(region[i-1].list_pos)+len(region[i].list_pos)]
    
 
    def make_tree(self, pos_vec):
        pos_vec = np.array([np.real(pos_vec), np.imag(pos_vec)]).T   
        return spp.cKDTree(pos_vec)
        
    def get_hood(self, point, tree):     
        return tree.query_ball_point(point, r=self.radius)
