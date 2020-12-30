# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 22:33:28 2020

@author: jgfri
"""

import random as rd
import numpy as np
from scipy import optimize
#jobs : farmer, 

class Person:
    def __init__(self):
        name = "Ted"
        culture = rd.randint(0,2)
        job = "Farmer"
        health = .75        
        money = 0
        leisureRatio = .25
        
        
        self.attributes = {"name": name, "culture": culture, "job": job, "jobwage": None,
                           "health": health, "leisureRatio": leisureRatio}
        self.resources = {"money": money}
        
        # I should put description here, but eh
        self.updateJobWage()
        
    def updateJobWage(self):
        if self.attributes["job"] == "Farmer":
            self.attributes["jobwage"] = 1
        else:
            self.attributes["jobwage"] = None
            
        
    def workJob(self):
        labor, leisure = self.allocateTime()
        
        self.resources["money"] += self.attributes["jobwage"] * labor
        
    def allocateTime(self):
        # huh may want to just cheat with cobb douglas
        # also note: update to prevent accidental minimization
        alpha = self.attributes["leisureRatio"]
        wage = self.attributes["jobwage"]
        max_hours = 16*self.attributes["health"]
    
        def f(x):
            return -(((max_hours-x)**alpha)*(wage*x)**(1-alpha))


        result = optimize.minimize_scalar(f,bounds=(0,max_hours), method='bounded')
        # rounds to one decimal
        labor_hours = round(result.x,1)
        leisure_hours = max_hours - labor_hours
        
        return (labor_hours,leisure_hours)
    
    def consumeGoods(self):
        money = self.resources["money"]
        
        if money > 4:
            self.attributes["health"] += .2
            self.resources["money"] -= 4
        else:
            self.attributes["health"] += (money-2)/10
            self.resources["money"] = 0
            
        if self.attributes["health"] > 1:
            self.resources["health"] = 1
        
        
            
        
class Tax:
    def __init__(self,subset_keys,subset_values,subset_conditions,tax_name):
        self.attributes = {"subset_keys": subset_keys, "subset_values":
                           subset_values, "subset_conditions": subset_conditions,
                           "tax_name": tax_name}
            
    def taxPerson(self,person):
        notEligibleForTax = False
        for index, subset_key in enumerate(self.attributes["subset_keys"]):
            if type(self.attributes["subset_values"][index]) == int or type(self.attributes["subset_values"][index]) == str:
                if self.attributes["subset_conditions"][index] == ">":
                    if person.attributes[subset_key] > self.attributes["subset_values"][index]:
                        notEligibleForTax = True
                elif self.attributes["subset_conditions"][index] == "=":
                    if person.attributes[subset_key] == self.attributes["subset_values"][index]:
                        notEligibleForTax = True
                elif self.attributes["subset_conditions"][index] == "<":
                    if person.attributes[subset_key] < self.attributes["subset_values"][index]:
                        notEligibleForTax = True
                else:
                    print("error in condition")
            elif type(self.attributes["subset_values"][index]) == list:
                if person.attributes[subset_key] in self.attributes["subset_values"][index]:
                    notEligibleForTax = True                
            else:
                print("error in type")
            
        
        eligibleForTax = not notEligibleForTax
        return eligibleForTax
        
    
        
class Game:
    def __init__(self):
        self.people = [Person() for i in range(0,100)]
        self.taxes = []
        

    def work(self):
        for person in self.people:
            person.workJob()
            
    def tax(self):
        for person in self.people:
            for tax in self.taxes:
                person = tax.taxPerson()
                
    def consume(self):
        for person in self.people:
            person.consumeGoods()
            
    def nextTick(self):
        self.work()
        self.consume()
        