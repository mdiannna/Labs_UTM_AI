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
    
    
    def is_negative(self):
        """ returns boolean, true if is negative """
        return (self.norm()<0)
             
    def to_list(self):
        return list(self.data)

a = Vector(1,2)    
b = Vector(2,2)    
print(b - a)

print(a)
print(a.to_list())
print(type(a))
print(type(b-a))
print("b:", b)
print("norml of b:", b.norm())
print("b is negative?", b.is_negative())