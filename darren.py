__author__ = 'tbrooks'

dark = 0.5
brown = 0.3
white = 0.0
black = 1.0


class Person:
    def __init__(self, name=None, height=None, weight=None, color=None):
        self.name = name
        self.height = height
        self.weight = weight
        self.color = color

    def __str__(self, *args, **kwargs):
        return self.name+' is '+str(self.height)+' feet tall.'

    def set_height(self, height):
        self.height = height


darren = Person(name='Darren', height=5.8, weight=150, color=dark)
trey = Person(name='Trey', height=5.9, weight=183, color=white)
darren.set_height(6.0)

print darren, trey