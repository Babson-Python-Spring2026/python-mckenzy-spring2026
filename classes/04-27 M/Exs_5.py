class Vehicle:
    def __init__(self, name):
        self.name = name
    

    def __str__(self):
        return "I'm and electric vehicle"
    
    def moves(self):
        print("I'm moving")
    
class Boat(Vehicle):

    def __init__ (self,name):
        super().__init__(name)

    def moves(self):
        print('sailing')

class Car(Vehicle):

    def __init__ (self,name):
        super().__init__(name)

    def moves(self):
        print('driving')

betsy = Car('betsy')
avrora = Boat('Avrora')
transports = [betsy,avrora]

for t in transports:
    t.moves()