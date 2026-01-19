import csv
import sys
sys.path.append("./functions")
import functions as fn

def read_track(file):
    with open("./tracks/"+file+".txt", 'r') as f:
        track_reader = csv.reader(f)
    return track_reader

def region_builder(reader):
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
    return regions


read_track(file = "race_track")
