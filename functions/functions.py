import numpy as np

class space:
    def __init__(self, bounds==[0,1], timeStep==1):
        self.bounds = bounds
        self.area =(bounds[0])*(bounds[1])
        self.normals =   [0+1j, #bottom boundary 
                         -1+0j, #right boundary
                          0-1j, #top boundary
                          1+0j] #left boundary
        self.shifts = [0j,1,1j,0]
        self.timeStep = timeStep

class manifest:
    def __init__(self, N == 1, space):
        self.vel = []
        self.pos = []

    def check_Pos(self, space): 
        # Makes an Nx4 matrix. Each column corresponds to a check for each boundary.
        # Positive values correspond to positions outside the simulaion bounds.
        checks_matrix = np.real(np.outer(self.pos-space.shifts, space.normals)) 
        return checks_matrix

    def step(self, space): 
        self.pos = self.pos + self.vel*space.timeStep
        self.enforceBoundary()
        self.computeVelocities()
        
    def enforceBoundary(self, space):
        checks_matrix_bool = self.check_Pos(space) > 0
    for i in range(len(space.normals))::
            
            

# Create a mask for manipulating the velocity and position vectors.
        


        

