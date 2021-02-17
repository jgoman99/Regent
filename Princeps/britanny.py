# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 21:14:20 2021

@author: jgfri
"""
import random as rd
import numpy as np

class Tile:
    def __init__(self, id_num):
        self.id = id_num
        self.wealth = 5
        self.owner_id = None

class Person:
    def __init__(self,id_num,loc):
        self.loc = loc
        self.id = id_num
        self.social = {}
        self.land = ()
        self.liege = {}
    
    def knowPerson(self, Person):
        if Person.id in self.social.keys():
            return True
        else:
            return False
        
    def meetPerson(self, Person):
        if not self.knowPerson(Person):
            self.social[Person.id] = 0
            Person.social[self.id] = 0
            
    def modifyRelationship(self,Person,modifier):
        # first checks if you know person, then meets the person
        self.meetPerson(Person)
        self.social[Person.id] = modifier
        
        
        

class Game:
    def __init__(self):
        self.mapWidth = 4
        self.mapHeight  = 5
        self.map = [[Tile((i,j)) for i in range(self.mapWidth)] for j in range(self.mapHeight)]
        self.map = np.reshape(self.map, (self.mapHeight,self.mapWidth))
        self.people = [Person(i,{"x":rd.randint(0, self.mapWidth-1),
                                 "y": rd.randint(0, self.mapHeight-1)}) for i in range(10)]
        
    def returnPopMap(self):
        new_map = np.zeros((self.mapHeight,self.mapWidth))
        for person in self.people:
            new_map[person.loc["y"]][person.loc["x"]] += 1
        
        return new_map
    
                    
        
    def distributeLand(self):
        # remember matrix is height x width
        for person in self.people:
            owner_id = self.map[person.loc["y"]][person.loc["x"]].owner_id
            if owner_id == None:
                self.map[person.loc["y"]][person.loc["x"]].owner_id = person.id
                person.land = (person.loc["y"],person.loc["x"])
            else:
                person.liege["landlord"] = owner_id
                
                
g1 = Game()
        