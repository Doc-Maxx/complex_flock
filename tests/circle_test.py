import sys
sys.path.append("./functions")
import functions as fn 
import numpy as np

point = np.array([1+1j, 1-1j, 1+1.5j])
circle = fn.circle(origin= 1+1j,radius =1)

print(circle.vec_within(point))

