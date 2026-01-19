import sys
sys.path.append("./functions")
import functions as fn
import numpy as np

N = 100
box = fn.rectangle(origin=3+0j, point_2 = 1+0j,  thickness=1)
mani = fn.manifest(1)
s = fn.space([box], mani, 1)
mani.spawn_flockers(N, s.regions[0])
mani.split_flockers(s)
if len(mani.pos_master) == N:
    print("Bulk Spawn Test: Success")
else:
    print("Bulk Spawn Test: Failure")
