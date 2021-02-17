import random as rd
import numpy as np

class Tile:
    def __init__(self, id_num):
        self.id = id_num
        self.capacity = 5
        self.owner_id = None

class Person:
    def __init__(self,id_num,loc):
        self.loc = loc
        self.id = id_num
        #opinion is on scale -100 to 100. 50 is good friends, 25 is friendly, 0 is neutral, -25 is 
        #minor enemies, - 50 is enemies, -75 is really bad enemies
        self.social = {}
        self.land = ()
        self.liege = {}
        
        self.job = {"job": None}
        self.resources = {"food": 0}
    
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
    
    def changeJob(self,newJob):
        self.job["job"] = newJob
        
    def workJob(self,Game):
        if self.job["job"] == "peasant":
            self.resources["food"] += 5
        s
        
        
        

class Game:
    def __init__(self):
        num_people = 100
        self.mapWidth = 4
        self.mapHeight  = 5
        self.map = [[Tile((i,j)) for i in range(self.mapWidth)] for j in range(self.mapHeight)]
        self.map = np.reshape(self.map, (self.mapHeight,self.mapWidth))
        self.people = [Person(i,{"x":rd.randint(0, self.mapWidth-1),
                                 "y": rd.randint(0, self.mapHeight-1)}) for i in range(num_people)]
        
    def returnMapType(self,mapType):
        new_map = np.zeros((self.mapHeight,self.mapWidth))
        if mapType == "num_people":
            for person in self.people:
                new_map[person.loc["y"]][person.loc["x"]] += 1
        elif mapType == "owner_id":
            for idy,row in enumerate(self.map):
                for idx, tile in enumerate(row):
                    owner_id = tile.owner_id
                    new_map[idy][idx] = owner_id  
        elif mapType == "capacity":
            for idy,row in enumerate(self.map):
                for idx, tile in enumerate(row):
                    capacity = tile.capacity
                    new_map[idy][idx] = capacity  
        else:
            return None
        return new_map
    
                    
        
    def distributeLand(self):
        # remember matrix is height x width
        for person in self.people:
            owner_id = self.map[person.loc["y"]][person.loc["x"]].owner_id
            if owner_id == None:
                self.map[person.loc["y"]][person.loc["x"]].owner_id = person.id
                person.land = (person.loc["y"],person.loc["x"])
                person.changeJob("landlord")
            else:
                person.liege["landlord"] = owner_id
                liege = self.people[[person.id for person in self.people].index(owner_id)]
                person.modifyRelationship(liege, 20)
                liege.modifyRelationship(person, 5)
                person.changeJob("peasant")
                
g1 = Game()
g1.distributeLand()
        