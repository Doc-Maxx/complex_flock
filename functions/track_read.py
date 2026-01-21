import csv
import sys
sys.path.append("./functions")
from functions import functions as fn
import numpy as np

def read_track(file):
    with open("./tracks/"+file+".txt", 'r') as f:
        track_reader = csv.reader(f)
        return region_builder(track_reader, file)

def region_builder(reader, file):
    track_reader = reader
    regions = []
    for row in track_reader:
        if row[0] == "rectangle":
            new = rect_row_reader(row)
            regions.append(new)
        elif row[0] == "circle":
            new = circle_row_reader(row)
            regions.append(new)
        elif row[0] == "ring":
            new = ring_row_reader(row)
            regions.append(new)
    print("Track: "+file+" built." + " Region list length: "+str(len(regions)))
    return regions

def rect_row_reader(row):
    origin = complex(row[1].replace(" ", ""))
    p2 = complex(row[2].replace(" ", ""))
    thickness = float(row[3])
    bound = str_to_bool(row[4])
    return fn.rectangle(origin = origin, point_2=p2, thickness = thickness, boundary_bool=bound)

def circle_row_reader(row):
    origin = complex(row[1].replace(" ", ""))
    radius = float(row[2])
    arc = np.array([degree_to_radian(float(row[3])), degree_to_radian(float(row[4]))])
    bound = str_to_bool(row[5])
    return fn.circle(origin=origin, radius=radius, arc = arc, boundary_bool=bound)
def ring_row_reader(row):
    origin = complex(row[1].replace(" ", ""))
    radius_i = float(row[2])
    radius_o = float(row[3])
    arc = np.array([degree_to_radian(float(row[4])), degree_to_radian(float(row[5]))])
    bound = str_to_bool(row[6])
    return fn.ring(origin=origin, radius_inner= radius_i, radius_outer=radius_o, arc = arc, boundary_bool=bound)

def degree_to_radian(ang):
    return ang * (2*np.pi / 360)

def str_to_bool(str):
    str = str.replace(" ", "")
    if str == "True":
        return True
    elif str == "False":
        return False
    else:
        print("Error: Bool passed might not be capitalized")    
