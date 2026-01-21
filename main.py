import sys
sys.path.append("functions/")
from functions import functions as fn
from functions import track_read as rd
import numpy as np
file = "race_track"

N = 5
steps = 100
r = rd.read_track(file)
m = fn.manifest(0.1,0.1)
s = fn.space(r,m,0.1)

m.spawn_flockers(N, r[0])
in2 = m.pos_master
for i in range(steps):
    m.step(s)
    m.split_flockers(s)
    m.enforce_boundary(r)
    m.reform_master_list(s)
    m.update_velocity(s)
    
#print(m.pos_master - in2)
print("aaa")
for i in s.regions:
    print((i.list_vel))
    print(i.type)
