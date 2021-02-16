import time
import random

""" Singleton class to Driver behaviour changes"""
class BehaviourChangeDriver:
    class __BehaviourChangeDriver:
        def __init__(self, arg):
            self.behaviour = arg
            self.last_time_behaviour_changed = time.time()
        def __str__(self):
            return repr(self) + self.behaviour
        def change_behaviour(self):
            possible_behaviours = ["normal", "attacking", "evading"]
            new_behaviour = random.choice(possible_behaviours)

            while new_behaviour==self.behaviour:
                new_behaviour = random.choice(possible_behaviours)
            
            print("behaviour changed to:", new_behaviour)
            self.behaviour = new_behaviour

    instance = None

    def __new__(cls, arg): # __new__ always a classmethod
        if not BehaviourChangeDriver.instance:
            BehaviourChangeDriver.instance = BehaviourChangeDriver.__BehaviourChangeDriver(arg)
        else:
            BehaviourChangeDriver.instance.behaviour = arg

        return BehaviourChangeDriver.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
    
    def change_behaviour(self):
        BehaviourChangeDriver.instance.change_behaviour()


# For testing:
if __name__=="__main__":
    x = BehaviourChangeDriver('normal')

    # print(x.last_time_behaviour_changed)
    print("Initial behaviour:", x.behaviour)

    while 2<3:
        if time.time() - x.last_time_behaviour_changed >=3:
            x.change_behaviour()
            x.last_time_behaviour_changed = time.time()
            print("current beh:", x.behaviour)

            