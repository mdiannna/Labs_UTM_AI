############################################################
################       utils.py            ###############
############################################################
def calcDistance(pos1, pos2, distance="euclidean"):
        """ 
        calculates the distance between 2 objects (now only euclidean distance)
        ------
        parameters:
            pos1(list[2]) - the position of first object
            pos2(list[2]) - the position of second object
            distance(str) - the type of distance, by default euclidean
        ------
        returns:
            dist(float) - the distance between objects
        """
        dist = sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
        return dist

def calcDistanceWithRadius(pos1, pos2, radius, distance="euclidean"):
        """ 
        calculates the distance between 2 objects (now only euclidean distance),
            but takes into account the radius of the object as well,
            assuming that both objects have the same radius
        ------
        parameters:
            pos1(list[2]) - the position of first object
            pos2(list[2]) - the position of second object
            radius(int or float) - the radius of one object
            distance(str) - the type of distance, by default euclidean
        ------
        returns:
            dist(float) - the distance between objects, or 0 if object (images) are intersecting
        """

        dist = sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2) - 2*radius
        #verify not to be negative distance
        return max(0,dist)

def get_all_positions(object_group):
    """
    gets all positions list for the objects group
    """
    all_positions = []
    for object in object_group:
        all_positions.append(object.get_pos())

    return all_positions

####################### end utils.py #######################