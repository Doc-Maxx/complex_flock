import sys
sys.path.append("./functions")
import functions as fn
import numpy as np

points = np.array([0.5 + 0.5j , 1.5 + 1.5j])
ring = fn.ring(origin=0+0j, radius_inner=1,radius_outer=3,arc=np.array([0,np.pi]))

res = ring.vec_within(points)
if res[0]==False and res[1]==True:
    print("Ring Test: Success")
else:
    print("Ring Test: Failure")
