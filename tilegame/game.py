# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 12:56:34 2020

@author: jgfri
"""

import random as rd

class Tile():
    def __init__(self):
        self.terrain = rd.randint(0,1)
        self.name = "ruthsberg"
                
            
        

class Person():
    def __init__(self):
        self.name = "Bill"
        self.tribe = rd.randint(0, 1)
        

class Game():
    def __init__(self):
        #game settings
        self.map_width = 4
        self.map_height = 8
        self.starting_people = 11
        
        
        self.map = [[Tile for i in range(self.map_height)] for j in range(self.map_width)]
        self.people = [Person() for i in range(0,self.starting_people)]