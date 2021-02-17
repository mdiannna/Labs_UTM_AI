############################################################
################        vector.py            ###############
############################################################
class Vector( object ):
    def __init__(self, *data):
        """ initialize vector with data """
        self.data = data
        
    def __repr__(self):
        """ returns representation of a vector """
        return repr(self.data) 
    
    def __add__(self, other):
        """ addition operator overload - implements operation of 2 vectors addition (sum) """
    
        return Vector(*list( (a+b for a,b in zip(self.data, other.data) ) ) )

    def __sub__(self, other):
        """ substraction operator overload - implements operation of 2 vectors substraction """

        return Vector(*list(a-b for a,b in zip(self.data, other.data) ) )
    
    def __div__(self, coefficient):
        """ division operator overload - implements vector multiplication with coefficient """
        new_data = map(lambda x: x/coefficient, self.data)
        return Vector(*new_data)
    
    def __mul__(self, coefficient):
        """ multiplier operator overload - implements vector multiplication with coefficient """
        new_data = map(lambda x: x*coefficient, self.data)
        return Vector(*new_data)
    
    def __rmul__(self, coefficient):
        """ right multiplier operator overload - implements right vector multiplication with coefficient """
        new_data = map(lambda x: coefficient*x, self.data)
        return Vector(*new_data)
        
    def __str__(self):
        """ convert to string """
        return str(list(self.data))

    def norm(self, p=2):
        """ 
            Calculate the p-norm of the vector, default p=2 (euclidean) 
            ----------
            parameters:
                p(int) - the p for the p-norm, default 2
            returns:
                _(int) - the norm of the vector
        """
        sum = 0
        for x in self.data:
            sum += x**p
        
        return sum**(1/p)
    
    def is_negative(self):
        """ returns boolean, true if is negative """
        return (self.norm()<0)
             
    def to_list(self):
        """ convert vector to list """
        return list(self.data)

####################### end vector.py #######################