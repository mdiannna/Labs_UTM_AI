### https://py3.codeskulptor.org/

############### Code for flocking behaviour ############3
from math import sqrt



def calculateDistance(pos1, pos2, distance="euclidean"):
        """ calculates the distance between 2 objects """
        dist = sqrt((pos1[0]-pos2[0])^2 + (pos1[1]-pos2[1])^2)
        return dist


print(calculateDistance([704, 473], [680, 333]))


# def separation(current_pos, all_positions):
#     """ steer to avoid crowding neighbours (short range repulsion) """
#     #min distance between rocks required
#     delta_distance = 2

#     # close_rocks = []
#     # for i in range(len(all_positions)):
#     #     for j in range(i+1, len(all_positions)):
#     #         dist_i_j = calculateDistance(rock_position_i, rock_position_j)
#     #         if dist_i_j < delta_distance:
#     #             close_rocks.append([i,j])

#     first_occurence = False
#     collision_with_pos = []

#     for i in range(len(all_positions)):
#         rock_i_pos = all_positions[i]
#         if rock_i_pos ==current_pos and first_occurence==True:
#             colision_with_pos.append(rock_i_pos)
#         elif rock_i_pos==current_pos and first_occurence==False:
#             first_occurence=True
#         else:
#             dist_i_j = calculateDistance(rock_i_pos, current_pos)
#             if dist_i_j < delta_distance:
#                 collision_with_pos.append(rock_i_pos)
#
#     print("Colisions with positions:", collision_with_pos)


    
def separation(all_positions):
    """ steer to avoid crowding neighbours (short range repulsion) """
    #min distance between rocks required
    delta_distance = 10

    close_rocks = []
    len_all_pos = len(all_positions)
    for i in range(len_all_pos):
        for j in range(i+1, len_all_pos):
            dist_i_j = calculateDistance(all_positions[i], all_positions[j])
            if dist_i_j < delta_distance:
                close_rocks.append([i,j])

                
    print("---Close rocks:", close_rocks)


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

# def getNewPos(current_pos, all_positions):
#     """ get the new position where the boid needs to move to """
#     separation(current_pos, all_positions)
    
#     # TODO


########### possible approach:
# fiecare din functii va returna "steering", directia cu cat sa mearga
# def updateOneBoid(self, all_boids):
#     alignment = self.alignment(boids)
#     cohesion = self.cohesion(boids)
#     separation = self.separation(boids)

#     self.acceleration += alignment
#     self.acceleration += cohesion
#     self.acceleration += separation

####3 general algo
# for boid in flock:
#     boid.show()
#     boid.apply_behaviour(flock)
#     boid.update()
#     boid.edges()
#### TODO: return to class Boid

def modelFlockingBehaviour(sprite_group):
    """ main algorithm here """
    new_sprite_group = set()
    
    all_positions = get_all_positions(sprite_group)
    print("all_positions:", all_positions)

    # TODO: finish
    separation(all_positions)

    for sprite in sprite_group:
        for i in range(DIMENSIONS):
            sprite.pos[i] %= CANVAS_RES[i]        

        sprite.pos[0] += 1 * random.choice([1,-1])
        sprite.pos[1] += 2 * random.choice([1,-1])

        # print("rock position:", sprite.get_pos())
        

        #############
            
        sprite.angle += sprite.angle_vel 
    
    return new_sprite_group
    
###########################################################