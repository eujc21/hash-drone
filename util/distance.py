import math
def distance(p0, p1):
    # This function takes different map coords and finds the euclidean distance
    # this function is necessary for determining the turns the drones take
    # the distance will be the main factor in how many turns are completed for each simulation
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)
