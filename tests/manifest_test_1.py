import sys
sys.path.append("./functions")
import functions as fn 
import numpy as np

r1 = fn.rectangle(origin=0+0j, point_2=1+0j,thickness=1)
r2 = fn.rectangle(origin=1+0j, point_2=2+0j,thickness=1)
m1 = fn.manifest()

m1.add_flocker(0.5+0.5j,0+0j)
m1.add_flocker(1.5+0.5j,0+0j)

print(m1.pos_master)
regions = [r1,r2]
m1.split_flockers(regions)

print(r1.points)
print(r1.list_pos)
print(r2.points)
print(r2.list_pos)
