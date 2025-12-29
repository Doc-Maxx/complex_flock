
import sys
sys.path.append("./functions")
import functions as fn

test_wall = fn.wall(1+1j,2+2j,1)

if test_wall.slope == 1 and test_wall.ori == -1+1j:
    print("Wall Test: Success/n")
else:
    print("Wall Test: Failure/n")
