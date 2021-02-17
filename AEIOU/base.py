# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 23:32:07 2021

@author: jgfri
"""
#imports
from scipy.stats import binom
import numpy as np

# this is too cpu heavy :(
# Global Vars (Move these later)
id_counter = 0
def updateIdCounter():
    global id_counter
    id_counter += 1

class Game:
    def __init__(self):
        self.deathChance = 300000000
        self.agePenalty = 4
        self.localunits = [LocalUnit()]
        
    def nextTick(self):
        for localunit in self.localunits:
            ageLocalUnit(localunit)
            arrangeMarriages(localunit)
            haveChildrenLocalUnit(localunit)

def findEntityById(unique_id):
    for localunit in g1.localunits:
        for person in localunit.people:
            if person.id == unique_id:
                return person



class LocalUnit:
    def __init__(self):
        self.people = peopleGenerator(1000)
        
def haveChildrenLocalUnit(localunit):
    couples = []
    for person in localunit.people:
        if 'spouse' in person.relations.keys():
            person1 = person
            person2 = findEntityById(person1.relations['spouse'])
            couples.append((person1,person2))
            
    couples = list(set(couples))
    for couple in couples:
        person1 = couple[0]
        person2 = couple[1]
        haveChild(person1,person2,localunit)
        

def ageLocalUnit(localunit):
    for person in localunit.people:
        ageOneYear(person)
        
        
def peopleGenerator(number):
    people = []
    for i in range(number):
        person = Person(id_counter)
        updateIdCounter()
        people.append(person)
        
    return people
        
def arrangeMarriages(localunit):
    dating_pool = []
    for person in localunit.people:
        # this is workaround should alter?
        if "spouse" not in person.relations.keys():
            dating_pool.append(person)
    
    #simple matching algorithm
    for idx in range(len(dating_pool)):
        if idx % 2 ==0:
            person1 = dating_pool[idx]
            person2 = dating_pool[idx+1]
            addRelation(person1,person2,"spouse","spouse")
        else:
            pass
            
        

class Person:
    def __init__(self,num_id):
        self.id = num_id
        self.ageInt = 18
        self.isAliveBool = True
        self.relations = {}
        
def haveChild(person1,person2,localunit):
    child = Person(id_counter)
    updateIdCounter()
    addRelation(person1,child,"parent","child")
    addRelation(person1,child,"parent","child")
    localunit.people.append(child)
    

def addRelation(person1, person2, relation1, relation2):
    person1.relations[relation1] = person2.id
    person2.relations[relation2] = person1.id
    
    
def ageOneYear(person):
    age = person.ageInt
    prob = (age**g1.agePenalty)/g1.deathChance
    flip = binom.rvs(1, prob, size=1)
    
    if flip == 1:
        person.isAliveBool = False
    else:
        person.ageInt += 1
        

#unvectorized, slow, so may need rewrite
def checkMeanAge():
    length = 1000
    age_list = [0]*length
    for i in range(length):
        age = 0
        while True:
            prob = (age**g1.agePenalty)/g1.deathChance
            flip = binom.rvs(1, prob, size=1)
            if flip == 1:
                age_list[i] = age
                break
            else:
                age += 1
        
    return(np.mean(age_list))
        
#initializes game here
g1 = Game()