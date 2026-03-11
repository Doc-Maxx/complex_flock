import numpy as np
import scipy.spatial as spp

def i_dot(vec1, vec2):
    return vec1 * np.conjugate(vec2)

def reflect(vec, mirror_vec):
    rot_angle = np.angle(mirror_vec) - np.angle(vec)
    return vec * np.e**(1j * rot_angle * 2)

def make_polygon_arc(origin, radius, corner_radius, ori, arc, N):
    lines_list = []
    angles = np.linspace(arc[0],arc[1], N)
    if ori == False:
        angles = np.flip(angles)
    points = origin + radius*np.e**(1j * angles)
    for i in range(N-1):
        lines_list.append(line(points[i], points[i+1], corner_radius))
    return lines_list

class line:
    def __init__(self, x1, x2):
        self.x = np.array([x1,x2])
        self.mag_x = np.abs(self.x)
        self.tangent = (self.x[1] - self.x[0])/np.abs(self.x[1] - self.x[0])
        self.normal = self.make_normal()
        self.region_projection = i_dot(self.x, self.tangent)
        self.angle = self.angle()
        self.x_prime = (self.x - self.x[0]) * np.e^(-1j * self.angle)

    def make_normal(self):
        return self.tangent*1j

    def angle(self):
        return np.angle(self.tangent)

class manifest:
    def __init__(self, interaction_radius, target_velocity, follow_factor=1, pressure_factor=0, lines):
        self.pos = np.array([])
        self.pos_last = np.array([])
        self.vel = np.array([])
        self.interaction_radius = interaction_radius
        self.target_velocity = target_velocity
        self.lines = lines
        self.follow_factor = follow_factor
        self.pressure_factor = pressure_factor

    def step(self, dt):
        self.pos = self.pos + self.vel*dt
        #self.enforce_boundary()
        self.update_velocity()

    def enforce_boundary(self):
        for i in lines:
            self.detection(i)
            self.disambiguation()
            self.reflect_pos()
            self.reflect_vel()

    def detection(line):
        before_ = i_dot(line.normal, self.pos_last)
        after_ = i_dot(line.normal, self.pos)
        before_bool = np.greater(before_, 0)
        after_bool = np.less_equal(after_, 0)
        return before_bool & after_bool



    def update_velocity(self):
        reg = self.regulate()
        tree = self.make_tree()
        fol = self.follow_neighbors(tree) * follow_factor
        pre = self.pressure(tree) * pressure_factor
        self.vel = reg + fol + pre

    def regulate(self):
        mags = np.abs(self.vel)
        fast_mask = np.where(mags>self.target_velocity*(1 + 0.03))
        slow_mask = np.where(mags<self.target_velocity*(1 - 0.03))
        vel_contribution = self.vel*0
        for i in self.vel[fast_mask]:
            vel_contribution[i] = i*(1-0.01)
        for i in self.vel[slow_mask]:
            vel_contribution[i] = i*(1+0.01)
        return vel_contribution

    def follow_neighbors(self, tree):
        vel = self.vel
        vel_contribution = self.vel*0
        for i in range(len(self.pos)):
            hood = self.get_hood(self.pos[i], tree)
            vel_contribution[i] = np.average(vel[hood])
        return vel_contribution

    def make_tree(self):
        pos_vec = np.array([np.real(self.pos), np.imag(self.pos)]).T
        print(pos_vec)
        return spp.cKDTree(pos_vec)

    def get_hood(self, pos, tree):
        return tree.query_ball_point(point, r = self.interaction_radius)

    def pressure(self, tree):
        vel_contribution = self.vel*0
        for i in range(len(self.pos)):
            hood = self.get_hood(self.pos[i], tree)
            pressure_vec = self.pos[hood] - self.pos[i]
            vel_contribution[i] = np.average(pressure_vec)
        return vel_contribution

    def spawn_flockers(self, N, origin, alignment='random'):
        positions = np.random.rand(N,2).view(np.complex128).flatten() + origin
        velocities = np.random.rand(N,2).view(np.complex128).flatten()

        self.pos = positions
        self.vel = velocities
