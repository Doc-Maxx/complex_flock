import sys
sys.path.append("./functions")
import functions as fn 
import numpy as np

point = np.array([1+1j, 1-3j, 1+1.5j,0.8+0.9j])
circle = fn.circle(origin= 1+1j,radius =1,arc=np.array([0,np.pi]))

vals=circle.vec_within(point)
if vals[0]==True and vals[1]==False and vals[2]==True and vals[3]==False:
    print("Circle Test: Success")
else:
    print("Circle Test: Failure")
