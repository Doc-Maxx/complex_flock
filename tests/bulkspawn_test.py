import sys
sys.path.append("./functions")
import functions as fn
import numpy as np

box = fn.rectangle(origin=3+0j, point_2 = 1+0j,  thickness=1)
mani = fn.manifest(1)
s = fn.space([box], mani, 1)
mani.spawn_flockers(10, s.regions[0])
mani.split_flockers(s)
print(len(s.regions[0].list_pos))
print(s.regions[0].list_pos)
