import numpy as np
import scipy.spatial as spp

def i_dot(vec1, vec2):
    return vec1 * np.conjugate(vec2)

def reflect(vec, mirror_vec):
    rot_angle = np.angle(mirror_vec) - np.angle(vec)
    return vec * np.e**(1j * rot_angle * 2)

def make_polygon_arc(origin, radius, ori, arc, N):
    lines_list = []
    angles = np.linspace(arc[0],arc[1], N)
    if ori == False:
        angles = np.flip(angles)
    points = origin + radius*np.e**(1j * angles)
    for i in range(N-1):
        lines_list.append(line(points[i], points[i+1]))
    return lines_list

class line:
    def __init__(self, x1, x2):
        self.x = np.array([x1,x2])
        self.mag_x = np.abs(self.x)
        self.tangent = (self.x[1] - self.x[0])/np.abs(self.x[1] - self.x[0])
        self.normal = self.make_normal()
        self.angle = self.angle()
        self.x_prime = (self.x - self.x[0]) * np.e**(-1j * self.angle)

    def make_normal(self):
        return self.tangent*1j

    def angle(self):
        return np.angle(self.tangent)

class manifest:
    def __init__(self, interaction_radius, target_velocity, follow_factor, pressure_factor, lines):
        self.pos = np.array([])
        self.pos_last = np.array([])
        self.vel = np.array([])
        self.interaction_radius = interaction_radius
        self.target_velocity = target_velocity
        self.lines = lines
        self.follow_factor = follow_factor
        self.pressure_factor = pressure_factor

    def step(self, dt):
        self.pos_last = self.pos
        self.pos = self.pos_last + self.vel*dt
        self.enforce_boundary()
        self.update_velocity()

    def enforce_boundary(self):
        for i in self.lines:
            detection_mask = self.detection(line= i)
            disambiguated_mask, x_int = self.disambiguation(i, detection_mask)
            pos_update, vel_update = self.reflect(i, disambiguated_mask, x_int)
            self.pos = pos_update
            self.vel = vel_update
    
    def detection(self, line):
        before_ = i_dot(line.normal, self.pos_last-line.x[0])
        after_ = i_dot(line.normal, self.pos-line.x[0])
        before_bool = np.greater(before_, 0)
        after_bool = np.less_equal(after_, 0)

        detection_bool = before_bool & after_bool
        return detection_bool

    def disambiguation(self, line, detection_mask):
        x_int = np.ones(len(detection_mask))*-1
        for i in range(len(detection_mask)):
            if detection_mask[i] == True:
                pos2 = (self.pos[i] - line.x[0])*np.e**(-1j * line.angle)
                pos1 = (self.pos_last[i] - line.x[0])*np.e**(-1j * line.angle)
                diff = pos2 - pos1
                if np.abs(np.real(diff)) < 1e-6:
                    x_int[i] = np.real(pos2)
                else:
                    m = np.imag(diff)/np.real(diff)
                    b = np.imag(pos1) - m * np.real(pos1)
                    x_int[i] = (m * np.real(pos1) - np.imag(pos1)) / m
        
        ambiguation_bool = np.logical_and(x_int>0, x_int<line.x_prime[1])
        disambiguated_mask = detection_mask & ambiguation_bool
       

        return disambiguated_mask, x_int

    def reflect(self, line, disambiguated_mask, x_int):
        pos2 = (self.pos - line.x[0])*np.e**(-1j * line.angle)
        vel_new = self.vel*np.e**(-1j * line.angle)
        for i in range(len(disambiguated_mask)):
            if disambiguated_mask[i] == True:
                pos2[i] = np.conjugate(pos2[i])
                vel_new[i] = np.conjugate(vel_new[i])
        pos3 = (pos2)*np.e**(1j * line.angle) + line.x[0]
        vel_new = vel_new*np.e**(1j * line.angle)
        return pos3, vel_new

    def update_velocity(self):
        tree = self.make_tree()
        fol = self.follow_neighbors(tree) * self.follow_factor
        pre = self.pressure(tree) * self.pressure_factor
        self.vel = fol + pre
        self.vel_reg()

    def vel_reg(self):
        np.where(self.vel > self.target_velocity*(1 + 0.03), self.vel*(1 - 0.1), self.vel )
        np.where(self.vel < self.target_velocity*(1 - 0.03), self.vel*(1+0.1), self.vel )

    def follow_neighbors(self, tree):
        vel = self.vel
        vel_contribution = self.vel*0
        for i in range(len(self.pos)):
            point =np.array([ np.real(self.pos[i]) , np.imag(self.pos[i])])
            hood = self.get_hood(pos = point, tree = tree)
            vel_contribution[i] = np.average(vel[hood])
        return vel_contribution

    def make_tree(self):
        pos_vec = np.array([np.real(self.pos), np.imag(self.pos)]).T
        return spp.cKDTree(pos_vec)

    def get_hood(self, pos, tree):
        return tree.query_ball_point(pos, r = self.interaction_radius)

    def pressure(self, tree):
        vel_contribution = self.vel*0
        for i in range(len(self.pos)):
            point =np.array([ np.real(self.pos[i]) , np.imag(self.pos[i])])
            hood = self.get_hood(point, tree)
            pressure_vec = self.pos[hood] - self.pos[i]
            vel_contribution[i] = np.average(pressure_vec)
       # vel_contribution = vel_contribution[:,0] + 1j * vel_contribution[:,1]
        return vel_contribution

    def spawn_flockers(self, N, origin, alignment='random'):
        positions = np.random.rand(N,2).view(np.complex128).flatten() + origin
        velocities = np.random.rand(N,2).view(np.complex128).flatten()

        self.pos = positions
        self.vel = velocities

    def add_flocker(self, pos, vel):
        self.pos = np.append(self.pos, pos)
        self.vel = np.append(self.vel, vel)
        
