class Boid():
    def __init__(self, initial_x, initial_y):
        """ initialize object """
        self.__x = initial_x
        self.__y = initial_y
        # TODO
    
    def calculateDistance(pos1, pos2, distance="euclidean"):
        """ calculates the distance between 2 objects """
        dist = sqrt((pos1[0]-pos2[0])^2 + (pos1[1]-pos2[1])^2)
        return dist

    
    def separation(current_pos, all_rocks_positions):
        """ steer to avoid crowding neighbours (short range repulsion) """
        #min distance between rocks required
        delta_distance = 2

        # close_rocks = []
        # for i in range(len(all_rocks_positions)):
        #     for j in range(i+1, len(all_rocks_positions)):
        #         dist_i_j = calculateDistance(rock_position_i, rock_position_j)
        #         if dist_i_j < delta_distance:
        #             close_rocks.append([i,j])

        bool first_occurence = False
        collision_with_pos = []

        for i in range(len(all_rocks_positions)):
            rock_i_pos = all_rocks_positions[i]
            if rock_i_pos ==current_pos and first_occurence==True:
                colision_with_pos.append(rock_i_pos)
            elif rock_i_pos==current_pos and first_occurence==False
                first_occurence=True
            else:
                dist_i_j = calculateDistance(rock_i_pos, current_pos)
                if dist_i_j < delta_distance:
                    collision_with_pos.append(rock_i_pos)
                    
        print("Colisions with positions:", collision_with_pos)
            
                
        
        # TODO: separate
    
    def alignment():
        """  steer towards the average heading of neighbours """
        pass
        # TODO
    
    def cohesion():
        """ steer to move towards average position of neighbours (long range attraction) """
        pass
        # TODO
    
    # def moveTo(self, new_x, new_y):
    #     """ move towards position new_x, new_y """
    #     pass
    #     # TODO
    
    # def moveBy(self, offset_x, offset_y):
    #     """ move by offset_x and offset_y """
    #     pass
    #     # TODO
    
    ######## practic aici va fi algoritmul de flocking
    def getNewPos(current_pos, all_rocks_positions):
        """ get the new position where the boid needs to move to """
        separation(current_pos, all_rocks_positions)
        
        # TODO
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
        
    @x.setter
    def x(self, new_x):
        self.__x = new_x
    
    @y.setter
    def y(self, new_y):
        self.__y = new_y


