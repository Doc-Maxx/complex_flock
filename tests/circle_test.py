import sys
sys.path.append("./functions")
import functions as fn 
import numpy as np

point = np.array([1+1j, 1-1j, 1+1.5j])
circle = fn.circle(origin= 1+1j,radius =1)

vals=circle.vec_within(point)
if vals[0]==True and vals[1]==False and vals[2]==True:
    print("Circle Test: Success")
else:
    print("Circle Test: Failure")
