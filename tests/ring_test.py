import sys
sys.path.append("./functions")
import functions as fn
import plotting as plot
import numpy as np

points = np.array([0.5 + 0.5j , 1.5 + 1.5j])
ring = fn.ring(origin=0+0j, radius_inner=1,radius_outer=3,arc=np.array([0,np.pi]),boundary_bool=True)

res = ring.vec_within(points)
if res[0]==False and res[1]==True:
    print("Ring Test: Success")
else:
    print("Ring Test: Failure")

m = fn.manifest(0.1,0.1)
r = [ring]
s = fn.space(r,m,1)
s.manifest.add_flocker(pos=points[0],vel=points[0])
steps=1
plot.plot(s, file = "ring_test_1")
print(s.manifest.vel_master)
print(s.manifest.pos_master)
print("--------------------")
for i in range(steps):
    m.step(s)
    m.split_flockers(s)
    m.enforce_boundary(r)
    m.reform_master_list(s)
    m.update_velocity(s)
    print(s.manifest.vel_master)
    print(s.manifest.pos_master)
    print("--------------------")

plot.plot(s, file = "ring_test_2")
