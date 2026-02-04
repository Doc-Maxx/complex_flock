import sys
sys.path.append("functions/")
from functions import physics as ph
from functions import plotting as plot
from functions import track_read as rd
import numpy as np

file = "race_track_gen2"

N = 40
lines = rd.read_track_gen2(file,0.05)
m = ph.manifest(0.1, 0.1, 1, 0, lines)
m.spawn_flockers(N, 0+0j)
dt = 1
steps = 10

plot.plot_gen2(m, file="test init")
for i in range(steps):
    m.step(dt)
plot.plot_gen2(m, file="test final")

