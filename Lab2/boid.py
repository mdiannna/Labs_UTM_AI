### https://py3.codeskulptor.org/

############### Code for flocking behaviour ############3
from math import sqrt
# import numpy as np


def calculateDistance(pos1, pos2, distance="euclidean"):
        """ calculates the distance between 2 objects """
        dist = sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
        return dist


# print(calculateDistance([704, 473], [680, 333]))

# https://stackoverflow.com/questions/534855/subtracting-2-lists-in-python

# https://stackoverflow.com/questions/534855/subtracting-2-lists-in-python
class Vector( object ):
    def __init__(self, *data):
        self.data = data
        
    def __repr__(self):
        return repr(self.data) 
        #return list(self.data) 
    
    
    def __add__(self, other):
        # return tuple( (a+b for a,b in zip(self.data, other.data) ) )  
        return Vector(*list( (a+b for a,b in zip(self.data, other.data) ) ) )
        #return Vector( (a+b for a,b in zip(self.data, other.data) ) )  

    def __sub__(self, other):
        # return tuple( (a-b for a,b in zip(self.data, other.data) ) )
        #return list( (a-b for a,b in zip(self.data, other.data) ) )
        return Vector(*list(a-b for a,b in zip(self.data, other.data) ) )
    
    def __div__(self, coefficient):
        new_data = map(lambda x: x/coefficient, self.data)
        return Vector(*new_data)
    
    def __mul__(self, coefficient):
        new_data = map(lambda x: x*coefficient, self.data)
        return Vector(*new_data)
    
    def __rmul__(self, coefficient):
        new_data = map(lambda x: coefficient*x, self.data)
        return Vector(*new_data)
    
    

        
    def __str__(self):
        return str(list(self.data))

    def norm(self, p=2):
        # result = 
        sum = 0
        for x in self.data:
            sum += x**p
        
        return sum**(1/p)
             
    def to_list(self):
        return list(self.data)


# a = Vector(1,2)    
# b = Vector(2,2)    
# print("B:", b)
# print(b/2)
# print(b - a)

# print(a)
# print(a.to_list())
# print(type(a))
# print(type(b-a))



class Boid:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        # self.pos =  np.array([pos[0],pos[1]])
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        # TODO:adjust as needed
        self.max_velocity = 5
        # self.vel = np.array([vel[0],vel[1]])
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.perception = 120

        if sound:
            sound.rewind()
            sound.play()
            
    def get_pos(self):
        return self.pos    

    def get_radius(self):
        return self.radius   
    
    def draw(self, canvas):
        if self.animated:
            new_image_center = [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, new_image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def separation(self, all_boids):
        """ steer to avoid crowding neighbours (short range repulsion) """
        #min distance between rocks required
        delta_distance = 120
        steer_vector = Vector(0, 0) # must be 2D vector
        avg_steer = Vector(0,0)
        steering = Vector(0,0)

        cnt_close_neigh = 0
        all_positions = get_all_positions(all_boids)

        for rock_i_pos in all_positions:
            dist_i_j = calculateDistance(rock_i_pos, self.pos)

            if dist_i_j>0 and dist_i_j < delta_distance:
                # TODO: process and add to steer_vector!
                print("!Colision at", rock_i_pos, "  ",  self.pos)
                # steer_vector = Vector(steer_vector) - Vector(Vector(*rock_i_pos) - Vector(*self.pos))
                diff = Vector(*rock_i_pos) - Vector(*self.pos)
                diff /= dist_i_j
                avg_steer += diff
                
                print("type diff:", type(diff))
                print("diff:", diff)
                # steer_vector = steer_vector + diff

                # print(type(steer_vector))
                # print("!!!! steer vector:", steer_vector)
                cnt_close_neigh +=1
            
        if cnt_close_neigh > 0:
            avg_steer /= cnt_close_neigh    

            #TODO: more
            steering = avg_steer - Vector(*self.vel)

        # print("Colisions with positions:", collision_with_pos)
        # print("!!!! steer vector:", steer_vector)
        # return steer_vector
        return steering


    #     Notice that in the loop for all the boids, we only look for boids at a certain distance —
    # that distance we call the
    # self.perception
    # (here it is equal to 100).
    def alignment(self, boids):
        """  steer towards the average heading of neighbours """
        avg_vector = Vector(0,0)
        steering = Vector(0,0)
        cnt_boids_in_perception = 0

        for boid in boids:
            if (Vector(*boid.pos)-Vector(*self.pos)).norm() < self.perception:
                avg_vector += Vector(*boid.vel)
                cnt_boids_in_perception +=1

        if cnt_boids_in_perception>0:
            avg_vector = avg_vector / cnt_boids_in_perception
            avg_vec_normalized = (avg_vector / avg_vector.norm()) 
            steering = avg_vec_normalized * (self.max_velocity/2) - Vector(*self.vel)
        
        return steering




    def cohesion(self, all_boids):
        """ steer to move towards average position of neighbours (long range attraction) """
        steering = Vector(0,0)
        cnt_boids_in_perception = 0
        center_mass = Vector(0,0)

        for boid in all_boids:
            if (Vector(*boid.pos)-Vector(*self.pos)).norm() < self.perception:
                center_mass += Vector(*boid.pos)
                cnt_boids_in_perception +=1
        
        if cnt_boids_in_perception>0:
            center_mass = center_mass / cnt_boids_in_perception
            diff_to_center_vect = center_mass - Vector(*self.pos)
            
            if diff_to_center_vect.norm() >0:
                diff_to_center_vect = (diff_to_center_vect/diff_to_center_vect.norm()) * self.max_velocity
            
            steering = diff_to_center_vect - Vector(*self.vel)

            # if steering.norm() > self.max_force:
            #     steering = (steering / steering.norm()) * self.max_force
        
        return steering


    def keep_on_screen(self):
        """ Keeps the object inside visible screen """
        for i in range(DIMENSIONS):
            self.pos[i] %= CANVAS_RES[i]      


    def add_steer(self, steer):
        if type(steer)==Vector:
            steer = steer.to_list()

        for i in range(DIMENSIONS):
            if steer[i]>0:
                self.pos[i] += max(1, int(steer[i]))
            elif steer[i]<0:
                self.pos[i] += min(-1, int(steer[i]))


    def add_negative_steer(self, steer):
        if type(steer)==Vector:
            steer = steer.to_list()
    
        for i in range(DIMENSIONS):    
            if steer[i]>0:
                    self.pos[i] -= max(1, int(steer[i]))
            elif steer[i]<0:
                self.pos[i] -= min(-1, int(steer[i]))

    ## Change later all_positions to neighbor_boids_positions
    def flocking_behaviour(self, all_boids):
        # steer = self.separation(all_boids)
        # # print("steer:", steer)
        
        # ##self.add_steer(steer)
        # self.add_negative_steer(steer)

        
        # steer = self.alignment(all_boids)
        # # print("steer:", steer)
        
        # self.add_steer(steer)
        
        steer = self.cohesion(all_boids)
        self.add_steer(steer)
        


    def update(self, all_boids):
        ###################!!!!
        # old code
        # for i in range(DIMENSIONS):
            ## makes the object re-appear to the other side of the canvas
            # self.pos[i] %= CANVAS_RES[i]
            ## Asta face ca toate sprites - roci, missile, sa se miste pe o linie inainte
            # self.pos[i] += self.vel[i]

        ## new experiments
        # for i in range(DIMENSIONS):
        #     self.pos[i] %= CANVAS_RES[i]        

        # self.pos[0] += 1 * random.choice([1,-1])
        # self.pos[1] += 2 * random.choice([1,-1])

        # print("rock position:", self.get_pos())
        # all_positions = get_all_positions(rock_group)
        # print("all_positions:", all_positions)

        # getNewPos(self.pos, all_positions)


        self.flocking_behaviour(all_boids)
        self.keep_on_screen()
        # #############
            
        # self.angle += self.angle_vel 
        self.age   += 1
        
        # return True if the sprite is old and needs to be destroyed
        if self.age < self.lifespan: 
            return False
        else:
            return True
    
    def collide(self, other_object):
        """
        Method that takes as imput a sprite and another object (e.g. the ship, a sprite)
        and returns True if they collide, else False
        """
        distance = dist(self.pos, other_object.get_pos())
        sum_radii = self.radius + other_object.get_radius()
        
        if distance < sum_radii:
            return True
        else:
            return False




    
# def separation(all_positions):
#     """ steer to avoid crowding neighbours (short range repulsion) """
#     #min distance between rocks required
#     delta_distance = 10

#     close_rocks = []
#     len_all_pos = len(all_positions)
#     for i in range(len_all_pos):
#         for j in range(i+1, len_all_pos):
#             dist_i_j = calculateDistance(all_positions[i], all_positions[j])
#             if dist_i_j < delta_distance:
#                 close_rocks.append([i,j])

                
#     print("---Close rocks:", close_rocks)


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

# def modelFlockingBehaviour(sprite_group):
#     """ main algorithm here """
#     new_sprite_group = set()
    
#     all_positions = get_all_positions(sprite_group)
#     print("all_positions:", all_positions)

#     # TODO: finish
#     separation(all_positions)

#     for sprite in sprite_group:
#         for i in range(DIMENSIONS):
#             sprite.pos[i] %= CANVAS_RES[i]        

#         sprite.pos[0] += 1 * random.choice([1,-1])
#         sprite.pos[1] += 2 * random.choice([1,-1])

#         # print("rock position:", sprite.get_pos())
        

#         #############
            
#         sprite.angle += sprite.angle_vel 
    
#     return new_sprite_group
    
###########################################################