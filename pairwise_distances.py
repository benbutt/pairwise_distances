#!/usr/bin/env python3

### pairwise_distances.py ###
### Ben Butt July 2020 by GNU GPLv3 ###

## From a list of coordinates as latitudes/longitudes, calculate and write a pairwise distance list ##
## Usage: ./pairwise_distances.py <samples.csv> ##
## Input format: Name,Latitude,Longitude as CSV with header line ##

# Import packages
import math
import sys

# Initialise dictionaries
sample_locs = {}
sample_dists = {}

# Grab filename from the argument
filename = sys.argv[1]
#print(filename)

# Read .csv and store sample locations as tuples
with open(filename, "r") as f:
    infile = f.read()
    for line in infile.strip().split("\n")[1:]:
        name = line.split(",")[0]
        lat = math.radians(float(line.split(",")[1]))
        long = math.radians(float(line.split(",")[2]))
        sample_locs[name] = (lat, long)

# Define Haversine function
def haversine(lat1, long1, lat2, long2):
    R = 6.371e6 # Radius of Earth in m
    dlon = abs(long2 - long1) # Longitude diff
    dlat = abs(lat2 - lat1) # Latitude diff
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2 # Haversine formula
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) # More Haversine
    return R * c

# Do the all-vs- all caluclations
for sample1 in sample_locs:
    for sample2 in sample_locs:
        if (sample1 + "_" + sample2) and (sample2 + "_" + sample1) not in sample_dists:
            lat1 = sample_locs[sample1][0]
            lat2 = sample_locs[sample2][0]
            long1 = sample_locs[sample1][1]
            long2 = sample_locs[sample2][1]
            sample_dists[sample1 + "_" + sample2] = haversine(lat1, long1, lat2, long2)

# Write out the distances
with open(filename.split(".")[0] + "_dists.csv", "w+") as outfile:
    outfile.write("Sample_pair, Distance(m)\n")
    for pair in sample_dists:
        outfile.write(pair + "," + str(sample_dists[pair]) + "\n")

print("Pairwise distances written to " + filename.split(".")[0] + "_dists.csv")
