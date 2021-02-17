# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 19:27:58 2021

@author: jgfri
"""
import random as rd

incomeTaxRate = .25
wages = 10
class Game:
    def __init__(self):
        self.nation = Nation()
        
        
    def nextTick:
        def __init__(self):
            self.workJob()
    def workJob:
        def __init__(self):
            for person in self.nation.people:
                
                if person.prisonBool:
                    continue
                
                
                job = person.job
                
                if job == "farmer":
                    person.money += wages*(1-incomeTaxRate)
                    self.nation.treasury += wages*incomeTaxRate
                elif job == "police":
                    person.money += wages*(1-incomeTaxRate)
                    self.nation.treasury += wages*incomeTaxRate
                    
                    workPoliceJob(person, self.nation.people)
                elif job == "diplomat":
                    person.money += wages*(1-incomeTaxRate)
                    self.nation.treasury += wages*incomeTaxRate
                elif job == "corruptionagent":
                    continue
                    
                    
def workPoliceJob(police,population):
    idx = [rd.randint(0,len(population)-1) for i in range(100)]
    for identity in idx:
        suspect = population[identity]
        investigateSuspect(police,suspect)       

def investigateSuspect(police,suspect):
    if suspect.job == "police":
        return
    if suspect.job == "thief":
        suspect.prisonBool = True
        
                    

class Person:
    def __init__(self):
        # Useless information
        self.name = 'r'
        
        #useful information
        self.culture = "red"
        self.religion = 'lyivism'
        
        self.culturalzeal = 0.4
        self.religiouszeal = 0.35
        self.nationalzeal = 0.25
        
        # civic information
        self.contentment = 0.75
        self.corruption = .5
        
        # other
        self.job = "farmer"
        self.prisonBool = False
        
        #resources
        self.money = 0
        
class Nation:
    def __init__(self):
        self.treasury = 1000
        
        self.people = [Person() for i in range(10000)]
        self.cabinet = {"Treasurer": Person(), "High Justice": Person(), "Security Chief": Person(),
                        "Senior General": Person(), "Chief Ambassador": Person()}
        
        self.allocation = {"treasury": .2, "defense":.35,"investigation": .15,"foreignrelations":.05,
                           "internalsecurity":.25}
        

class Company:
    def __init__(self):
        self
        
        
