import sys
sys.path.append("./functions")
import functions as fn
import numpy as np

point = np.array([-1 + 1j])
box = fn.rectangle(origin=-2 + 0j, point_2=0.5 +0.5j,thickness=3)

result= box.point_Within(point)
if result = True:
    print("Rectangle Test: Passed")
else:
    print("Rectangle Test: Failed")
