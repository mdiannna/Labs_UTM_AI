############################################################
################        boid.py            ###############
############################################################
class Boid:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.acceleration = [0,0]
        self.max_velocity = 2
        self.max_force = 0.25
        self.perception = 250
        self.behaviour_driver = BehaviourChangeDriver('normal')
        self.delta_s_change_behaviour = 7 #will change bbehaviour every 7 seconds

        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0

        if sound:
            sound.rewind()
            sound.play()
            
    def get_pos(self):
        """ 
        get position of boid 
        returns:
            list[2] - current position of boid
        """
        return self.pos    

    def get_radius(self):
        """ get radius of boid """
        return self.radius   
    
    def draw(self, canvas):
        """ draw boid on canvas """
        if self.animated:
            new_image_center = [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, new_image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def separation(self, all_boids):
        """ 
        steer to avoid crowding neighbours (short range repulsion) 
        ----------
        parameters:
            all_boids(set) - the set of all boids
        ----------
        returns:
            steering(Vector) - the steering vector to add to acceleration of boid
        """

        #min distance between rocks required
        delta_distance = self.perception
        steer_vector = Vector(0, 0) # must be 2D vector
        avg_steer = Vector(0,0)
        steering = Vector(0,0)

        cnt_close_neigh = 0
        all_positions = get_all_positions(all_boids)

        for rock_i_pos in all_positions:
            
            dist_i_j = calcDistanceWithRadius(rock_i_pos, self.pos, self.radius)

            
            if self.pos!=rock_i_pos and dist_i_j < delta_distance:
                #If rocks are intersecting, we consider the distance to be very very small, while the "diff" will still be the distance btw centers
                # so that the final "force" will be big
                if dist_i_j==0: #means rocks are intersecting
                    small_dist = 0.000001
                    dist_i_j = small_dist
                    diff = Vector(*self.pos) - Vector(*rock_i_pos)
                else:
                    diff = Vector(*self.pos) - Vector(*rock_i_pos) - self.radius * Vector(2,2)

                diff /= dist_i_j
                avg_steer += diff
                cnt_close_neigh +=1
            
        if cnt_close_neigh > 0:
            avg_steer /= cnt_close_neigh    

            steering = avg_steer - Vector(*self.vel)

        steering = self.adjust_steering_force(steering)

        return steering

    
    def alignment(self, boids):
        """  
        steer towards the average heading of neighbours 
        ----------
        parameters:
            boids(set) - the set of all boids
        ----------
        returns:
            steering(Vector) - the steering vector to add to acceleration of boid
        """
        avg_vector = Vector(0,0)
        steering = Vector(0,0)
        cnt_boids_in_perception = 0

        for boid in boids:
            distance = calcDistanceWithRadius(boid.pos, self.pos, self.radius)

            if (distance < self.perception):
                avg_vector += Vector(*boid.vel)
                cnt_boids_in_perception +=1

        if cnt_boids_in_perception>0:
            avg_vector = avg_vector / cnt_boids_in_perception
            avg_vec_normalized = (avg_vector / avg_vector.norm()) 
            steering = avg_vec_normalized * (self.max_velocity) - Vector(*self.vel)
    
        steering = self.adjust_steering_force(steering, delta_force=-0.01)

        return steering


    def cohesion(self, all_boids, delta_force=-0.01):
        """ 
        steer to move towards average position of neighbours (long range attraction) 
        ----------
        parameters:
            boids(set) - the set of all boids
            delta_force(float) - the max_force adjustment to add to increase or decrease max force
        ----------
        returns:
            steering(Vector) - the steering vector to add to acceleration of boid
        """
        steering = Vector(0,0)
        cnt_boids_in_perception = 0
        center_mass = Vector(0,0)

        for boid in all_boids:
            distance = calcDistanceWithRadius(boid.pos, self.pos, self.radius)
            if (distance < self.perception):

                center_mass += Vector(*boid.pos)
                cnt_boids_in_perception +=1
        
        if cnt_boids_in_perception>0:
            center_mass = center_mass / cnt_boids_in_perception
            diff_to_center_vect = center_mass - Vector(*self.pos)  - self.radius * Vector(1,1)
            
            if diff_to_center_vect.norm() >0:
                diff_to_center_vect = (diff_to_center_vect/diff_to_center_vect.norm()) * self.max_velocity
            
            steering = diff_to_center_vect - Vector(*self.vel)
        
        steering = self.adjust_steering_force(steering, delta_force=delta_force)
        
        return steering


    def adjust_steering_force(self, steering, delta_force=0):
        """
        function to adjust steering force - if the force exceeds max fore, then it is decreased
        -------
        parameters:
            steering(Vector) - the steering vector
            delta_force(float) - the max_force adjustment to add to increase or decrease max force
        returns:
            steering(Vector) - the steering vector with force adjusted
        """
        if steering.norm() > self.max_force:
            steering = (steering / steering.norm()) * (self.max_force+delta_force)
            
        return steering
        

    def keep_on_screen(self):
        """ Keeps the object inside visible screen """
        for i in range(DIMENSIONS):
            self.pos[i] %= CANVAS_RES[i]      


    def add_steer(self, steer):
        """ 
        adds steering to acceleration 
        --------
        parameters:
            steer(Vector) - the steering vector
        """
        if type(steer)==Vector:
            steer = steer.to_list()

        for i in range(DIMENSIONS):
            if steer[i]>0:
                self.acceleration[i] += max(1, int(steer[i]))
                
            elif steer[i]<0:
                self.acceleration[i] += min(-1, int(steer[i]))


    def add_negative_steer(self, steer):
        """ 
        adds negative steer to acceleration 
        --------
        parameters:
            steer(Vector) - the steering vector
        """
        if type(steer)==Vector:
            steer = steer.to_list()
    
        for i in range(DIMENSIONS):    
            if steer[i]>0:
                    self.acceleration[i] -= max(1, int(steer[i]))
            elif steer[i]<0:
                self.acceleration[i] -= min(-1, int(steer[i]))

        

    def flocking_behaviour(self, all_boids):
        """
        the function implementing flocking behaviour
        -------
        parameters:
            all_boids (set) - the set of all boids
        """
        align_steer = self.alignment(all_boids)
        cohesion_steer = self.cohesion(all_boids)
        sep_steer = self.separation(all_boids)
        
        self.add_steer(align_steer)
        self.add_steer(cohesion_steer)
        self.add_steer(sep_steer*2)



    def attacking_behaviour(self, other_objects, coef_steer=3):
        """
        implementing attacking behaviour - thrust asteroids towards a starship, aiming to collide and destroy them
        -------
        parameters:
            all_boids (set) - the set of all boids,
            coef_steer(int) - the coefficient to multiply the steering
        """
        cohesion_steer = self.cohesion(other_objects, delta_force=4)
        self.add_steer(cohesion_steer*coef_steer)


    def evading_behaviour(self, other_objects, coef_steer=5):
        """
        implementing evading behaviour - trying to evade any unknown objects, like starships and their missiles
        -------
        parameters:
            all_boids (set) - the set of all boids,
            coef_steer(int) - the coefficient to multiply the steering
        """
        separation_steer = self.separation(other_objects)
        self.add_steer(separation_steer*coef_steer)
        

    def update(self, all_boids, ship, other_objects):
        """ 
        update boid position and parameters
        ------
        parameters:
            all_boids (set) - the set of all boids
            ship (Ship) - the ship object
            other_objects(Sprite or obj) - other objects in the game, like ships, missiles etc
        --------
        returns:
            _(bool) - True if the sprite is old and needs to be destroyed
        """

        if time.time() - self.behaviour_driver.last_time_behaviour_changed >=self.delta_s_change_behaviour:
            self.behaviour_driver.change_behaviour()
            self.behaviour_driver.last_time_behaviour_changed = time.time()
            print("current beh:", self.behaviour_driver.behaviour)
        
        self.flocking_behaviour(all_boids)

        if self.behaviour_driver.behaviour=="attacking":
            self.attacking_behaviour([ship])

        elif self.behaviour_driver.behaviour=="evading":
            self.evading_behaviour(other_objects)


        self.pos = (Vector(*self.pos) + Vector(*self.vel)).to_list()
        self.vel  = (Vector(*self.vel) + Vector(*self.acceleration)).to_list()
        velocity_vect = Vector(*self.vel)

        if velocity_vect.norm() > self.max_velocity:
            self.vel = ((velocity_vect / velocity_vect.norm()) * self.max_velocity).to_list()

        self.acceleration = [0,0]

        self.keep_on_screen()            
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
        ---------
        parameters:
            other_object(Sprite or object) - other object to check if collision
        """
        distance = dist(self.pos, other_object.get_pos())
        sum_radii = self.radius + other_object.get_radius()
        
        if distance < sum_radii:
            return True
        else:
            return False

#################### end boids.py ######################

