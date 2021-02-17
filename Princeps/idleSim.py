# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 01:15:30 2021

@author: jgfri
"""
import random as rd
import numpy as np
from scipy.stats import distributions

class Person:
    def __init__(self,num_id,age):
        self.id = "person" + str(num_id)
        self.age = age
        self.sex = rd.randint(0,1)
        self.job = None
        self.relations = {}
        
    def birthday(self):
        self.age += 1
        


        
def addRelation(person1,person2,relation1,relation2):
    person1.relations[person2.id] = relation1
    person2.relations[person1.id] = relation2

# will later add same sex. This is just early 
def arrangeMarriages(town):
    males = []
    females = []
    for person in town.people:
        if ("spouse" not in person.relations.values()) & (person.age >= 18):
            if person.sex == 0:
                males.append(person)
            elif person.sex == 1:
                females.append(person)
    
    for idx, male in enumerate(males[0:len(females)]):
        female = females[idx]
        addRelation(male,female,"spouse","spouse")
        
            
def haveBaby(person1,person2,town):
    baby_id = len(town.people)
    baby = Person(baby_id,0)
    addRelation(person1, baby, "parent", "child")
    addRelation(person2, baby, "parent", "child")
    town.people.append(baby)
    
def ageTown(town):
    for person in town.people:
        person.birthday()
        
    
def arrangeBabies(town):
    married = []
    for person in town.people:
        if "spouse" in person.relations.values():
            married.append(person)
            
    for person in married:
        spouse_id = list(person.relations.keys())[list(person.relations.values()).index('spouse')]
        spouseEntity = getEntityFromId(spouse_id, town)
        married.remove(spouseEntity)
        haveBaby(person, spouseEntity, town)
        
def arrangeDeaths(town):
    mean_age_at_death = 80
    for person in town.people:
        # fix
        death_prob = distributions.expon.pdf(person.age,loc = mean_age_at_death, scale =1)
        
        if np.random.binomial(1,death_prob) == 0:
            personDies(person, town)
            
# removes references to person, and then removes person from list
def personDies(person,town):
    for relation in person.relation:
        relationEntity = getEntityFromId(relation, town)
        del relationEntity.relations[person.id]
    town.people.remove(person)
        
def getEntityFromId(entity_id,town):
    idx = [person.id for person in t1.people].index(entity_id)
    entity = town.people[idx]
    return(entity)

class Town:
    def __init__(self):
        self.people = [Person(i,120) for i in range(10)]
        
    def nextTick(self):
        arrangeMarriages(self)
        #arrangeBabies(self)
        ageTown(self)
        arrangeDeaths(self)
        

t1 = Town()
t1.nextTick()