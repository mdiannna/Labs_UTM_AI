
# https://stackoverflow.com/questions/534855/subtracting-2-lists-in-python
class Vector( object ):
    def __init__(self, *data):
        self.data = data
        
    def __repr__(self):
        return repr(self.data) 
        #return list(self.data) 
    
    
    def __add__(self, other):
        # return tuple( (a+b for a,b in zip(self.data, other.data) ) )  
        return list( (a+b for a,b in zip(self.data, other.data) ) )  
        #return Vector( (a+b for a,b in zip(self.data, other.data) ) )  

    def __sub__(self, other):
        # return tuple( (a-b for a,b in zip(self.data, other.data) ) )
        #return list( (a-b for a,b in zip(self.data, other.data) ) )
        return Vector(tuple(a-b for a,b in zip(self.data, other.data) ) )
        
    def __str__(self):
        return str(list(self.data))
        
    def to_list(self):
        return list(self.data)
   

a = Vector(1,2)    
b = Vector(2,2)    
print(b - a)

print(a)
print(a.to_list())
print(type(a))
print(type(b-a))