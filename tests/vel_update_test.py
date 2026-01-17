import sys
sys.path.append("./functions")
import functions as fn
import numpy as np

mani = fn.manifest(radius=10)
mani.add_flocker(0+0.5j,0+1j)
mani.add_flocker(0+0.6j,0+1j)
mani.add_flocker(-1+0.5j,0-1j)
mani.add_flocker(1+0.5j,0-1j)

r1 = fn.rectangle(-1.5+0j, -0.5+0j,1)
r2 = fn.rectangle(-.5+0j, 0.5+0j,1)
r3 = fn.rectangle(.5+0j, 1.5+0j,1)
regions = [r1,r2,r3]
s = fn.space(regions,mani, 1)
mani.split_flockers(s)
mani.update_velocity(s)
mani.reform_master_list(s)
if np.average(mani.vel_master) == 0+0j:
    print("Velocity Update Test: Success")
else:
    print("Velocity Update Test: Failure")
