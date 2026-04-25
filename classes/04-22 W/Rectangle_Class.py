class Rectangle:
    def __init__ (self,width):
        self.width = width
    @property
    def width(self):
        return self._width  

    @width.setter
    def width(self, value):
        self._width = value

r1 = Rectangle(7)

print(r1._width)





    
        