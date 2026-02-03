import numpy as np
import scipy.spatial as spp

def i_dot(vec1, vec2):
    return vec1 * np.conjugate(vec2)

def reflect(vec, mirror_vec):
    rot_angle = np.angle(mirror_vec) - np.angle(vec)
    return vec * e**(1j * rot_angle * 2)

def make_polygon_arc(origin, radius, corner_radius, ori=True, arc, N):
    lines_list = []
    angles = np.linspace(arc[0],arc[1], N)
    if ori == False:
        angles = np.flip(angles)
    points = origin + radius*e**(1j * angles)
    for i in range(N):
        lines_list.append(line(points[i], points[i+1], corner_radius))
    return lines_list

class line:
    def __init__(self, x1, x2, corner_radius):
        self.x = np.array([x1,x2])
        self.mag_x = np.abs(x)
        self.tangent = (self.x[1] - self.x[2])/np.abs(self.x[1] - self.x[2])
        self.normal = self.make_normal()
        self.region_projection = i_dot(self.x, self.tangent)
        self.angle = self.angle()
        self.corner_radius = corner_radius

    def make_normal(self):
        return self.tangent*1j

    def angle(self):
        return = np.angle(self.tangent)

    def get_region_masks(self, vec):
        p = i_dot(vec, self.tangent)
        r0_mask = p < self.region_projection[0]
        r1_mask = self.region_projection[0] < p < self.region_projection[1]
        r2_mask = self.region_projection[1] < p
        return r0_mask, r1_mask, r2_mask

    def distance(self, vec):
        d = np.array([])
        masks = self.get_region_masks(vec)
        for i in np.where(masks[0]):
            d[i] = vec - self.x[0]
        for i in np.where(masks[1]):
            d[i] = i_dot(vec, self.normal)
        for i in np.where(masks[2]):
            d[i] = vec - self.x[1]
        return d, masks

    def get_push_masks(self, distances, region_masks):
        masks = region_masks
        for i in np.where(region_masks[0]):
            if np.abs(distances[i]) > 2*self.corner_radius:
                masks[0][i] = False
        for i in np.where(region_masks[1]):
            if distances[i] > 0+self.corner_radius:
                masks[1][i] = False
        for i in np.where(region_masks[2]):
            if np.mag(distances[i]) > 2*self.corner_radius
                masks[2][i] = False
        return masks

    def push(self, pos, vel):
        distances, region_masks = self.distances(pos)
        masks = self.get_push_masks(distances, region_masks)
        self.corner_push(pos, vel, mask[0], distances)
        self.line_push(pos, vel, mask[1], distances)
        self.corner_push(pos, vel, mask[2], distances)

    def corner_push(self, pos, vel, mask, distances):
        overlap = 2* self.corner_radius - np.abs(distances)
        overlap_dir = distances / np.abs(distances)
        for i in pos[mask]:
            tangent = overlap_dir[i]*-1j
            vel[i] = reflect(i, tangent)
            pos[i] = pos[i] + overlap[i] * overlap_dir[i]

    def line_push(self, pos, vel, mask, distances):
        for i in pos[mask]:
            if i_dot(vec[i], self.normal) < 0:
                vec[i] = reflect(i, self.tangent)
            pos[i] = reflect(pos[i]-self.x[0], self.tangent) + self.x[0]

class manifest:
    def __init__(self, interaction_radius, target_velocity, follow_factor, pressure_factor, lines):
        self.pos = np.array([])
        self.vel = np.array([])
        self.interaction_radius = interaction_radius
        self.target_velocity = target_velocity
        self.lines = lines
        self.follow_factor = follow_factor
        self.pressure_factor = pressure_factor

    def enforce_boundary(self, lines):
        for i in lines:
            i.push(self.pos, self.vel)

    def update_velocity(self):
        reg = self.regulate()
        tree = make_tree()
        fol = self.follow_neighbors(tree) * follow_factor
        pre = self.pressure(tree) * pressure_factor
        self.vel = reg + fol + pre

    def regulate(self):
        mags = np.abs(self.vel)
        fast_mask = np.where(mags>self.target_velocity*(1 + 0.03))
        slow_mask = np.where(mags<self.target_velocity*(1 - 0.03))
        vel_contribution = self.vel*0
        for i in self.vel[fast_mask]:
            vel_contribution[i] = self.vel[i]*(1-0.01)
        for i in self.vel[slow_mask]:
            vel_contribution[i] = self.vel[i]*(1+0.01)
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

