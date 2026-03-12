import sys
sys.path.append("functions/")
from functions import physics as ph
from functions import plotting as plot
from functions import track_read as rd
import numpy as np

file = "race_track_gen2"

N = 20
lines = rd.read_track_gen2(file,0.05)
m = ph.manifest(0.1, 0.1, 1, 0, lines)
m.spawn_flockers(N, 0+0j)
#m.add_flocker(1+1j, 1+0j)
dt = 0.3
steps = 20

plot.plot_gen2(m, file="Test init")
for i in range(steps):
    m.step(dt)
    plot.plot_gen2(m, file="test step: " + str(i))
    #print([m.pos_last,m.pos,m.vel])
plot.plot_gen2(m, file="test final")

