class Boid():
    def __init__(self, initial_x, initial_y):
        """ initialize object """
        self.__x = initial_x
        self.__y = initial_y
        # TODO
    
    def separation():
        """ steer to avoid crowding neighbours (short range repulsion) """
        pass
        # TODO
    
    def alignment():
        """  steer towards the average heading of neighbours """
        pass
        # TODO
    
    def cohesion():
        """ steer to move towards average position of neighbours (long range attraction) """
        pass
        # TODO
    
    def moveTo(self, new_x, new_y):
        """ move towards position new_x, new_y """
        pass
        # TODO
    
    def moveBy(self, offset_x, offset_y):
        """ move by offset_x and offset_y """
        pass
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


