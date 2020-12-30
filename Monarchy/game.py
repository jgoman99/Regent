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
        job = "farmer"
        health = .75        
        money = 0
        
        
        self.attributes = {"name": name, "culture": culture, "job": job, "jobwage": None,
                           "health": health, "content" : 75}
        self.resources = {"money": money}
        self.instances = {"leisure_hours": None, "labor_hours": None }
        self.taxes = {"flat": 0, "prop": 0}
        
        
        # I should put description here, but eh
        self.updateJobWage()
        
    def updateJobWage(self):
        job = self.attributes["job"]
        if job == "farmer":
            self.attributes["jobwage"] = 1
        elif job == "thief":
            self.attributes["jobwage"] = 0
        else:
            self.attributes["jobwage"] = None
            
        
    def workJob(self,person):
        job = self.attributes["job"]
        if job == "farmer":
            self.allocateTime()
            labor = self.instances["labor_hours"]
            self.resources["money"] += self.attributes["jobwage"] * labor
        elif job == "thief":
            self.steal(person)
            
    def steal(self, people):
        health = self.attributes["health"]
        steal_chance = round((rd.random()+.49)*np.sqrt(health))
        
        if steal_chance == 1:
            amount = 4
            for person in people:
                if (amount > person.resources["money"]):
                    amount = person.resources["money"]
                
                person.resources["money"] -= amount
                self.resources["money"] += amount
        

        
        
    def allocateTime(self):
        # remember: weird stuff can happen with maximization, so check methods:       
        
        wage = self.attributes["jobwage"]
        max_hours = 16*self.attributes["health"]
        
        #fixes taxes to not cause sqrt errors:
        prop_tax = self.taxes["prop"]
        if  prop_tax > 1:
            prop_tax = 1
    
        # def f(x):
        #     return -(((max_hours-x)**alpha)*(wage*x)**(1-alpha))
        
        def f(x):
            return -(np.sqrt(max_hours-x) + np.sqrt((1-prop_tax)*wage*x))



        result = optimize.minimize_scalar(f,bounds=(0,max_hours), method='bounded')
        # rounds to one decimal
        labor_hours = round(result.x,1)
        leisure_hours = max_hours - labor_hours
        
        self.instances["leisure_hours"], self.instances["labor_hours"] = leisure_hours, labor_hours
    
    def consumeGoods(self):
        #may need to tweak content formula
        money = self.resources["money"]
        job = self.attributes["job"]
        
        if job == "farmer":
            if money > 4:
                self.attributes["health"] += .2
                self.resources["money"] -= 4
                self.attributes["content"] += 2
            else:
                self.attributes["health"] += (money-2)/10
                self.resources["money"] = 0
                self.attributes["content"] += (money-2)*10
                
            if self.attributes["health"] > 1:
                self.attributes["health"] = 1
            
            if self.attributes["content"] > 100:
                self.attributes["content"] = 100
        elif job == "thief":
            if money > 4:
                self.attributes["health"] += .2
                self.resources["money"] -= 4
            else:
                self.attributes["health"] += (money-2)/10
                self.resources["money"] = 0
         
            if self.attributes["health"] > 1:
                self.attributes["health"] = 1
            
        
        
    
    def updateJob(self):
        content, health = self.attributes["content"], self.attributes["health"]
        if content < 20 and health >= 0.5:
            self.attributes["job"] = "thief"
            
        self.updateJobWage()
            
            
            
        
class Tax:
    def __init__(self,subset_keys,subset_values,subset_conditions,tax_name,
                 tax_resource,tax_type,tax_amount):
        self.attributes = {"subset_keys": subset_keys, "subset_values":
                           subset_values, "subset_conditions": subset_conditions,
                           "tax_name": tax_name,"tax_resource": tax_resource, "tax_type": tax_type,
                           "tax_amount": tax_amount}
    #Tax(["culture","name"],[[0,2],"Ted"],["=","="],"xtax","money","flat",2)
    def isPersonTaxable(self,person):
        eligibleForTax = True
        for index ,subset_key in enumerate(self.attributes["subset_keys"]):
            subset_value = self.attributes["subset_values"][index]
            
            if type(subset_value) == list:
                if person.attributes[subset_key] not in subset_value:
                    eligibleForTax = False
            else:
                subset_condition = self.attributes["subset_conditions"][index]
                
                if (subset_condition == ">"):
                    if (person.attributes[subset_key] <= subset_value):
                        eligibleForTax = False
                elif (subset_condition == "="):
                    if (person.attributes[subset_key] != subset_value):
                        eligibleForTax = False
                elif (subset_condition == "<"):
                    if (person.attributes[subset_key] >= subset_value):
                        eligibleForTax = False
                else:
                    print("error")
                  
        return eligibleForTax
    
    def taxPerson(self, person):
        print(1)
        
        
    
        
class Game:
    def __init__(self):
        #currently up to 1000 people with all calculations done in less than a second
        self.people = [Person() for i in range(0,100)]
        self.taxes = []
        self.treasury = {"money": 0 }
        

    def work(self):
        for person in self.people:
            job = person.attributes["job"]
            victims = []
            # Yes you can steal from yourself. Meh. fine for sim reasons
            if job == "thief":
                victim1 = self.people[rd.randint(0,len(self.people)-1)]
                victim2 = self.people[rd.randint(0,len(self.people)-1)]
                victims.append(victim1)
                victims.append(victim2)
            person.workJob(victims)
            
    def taxPeople(self):
        for person in self.people:
            tax = 0
            prop_tax = person.taxes["prop"]*person.instances["labor_hours"]*person.attributes["jobwage"]
            flat_tax = person.taxes["flat"]
            tax = prop_tax + flat_tax
            if (person.resources["money"] < tax):
                self.treasury["money"] += person.resources["money"]
                person.resources["money"] = 0
                person.attributes["content"] -= 40
            else:
                self.treasury["money"] += tax
                person.resources["money"] -= tax
            
                
    def updateJobs(self):
        for person in self.people:
            person.updateJob()
            
            
            
    def updatePeoplesTaxes(self):
        for person in self.people:
            prop_tax = 0
            flat_tax = 0
            for tax in self.taxes:
                if tax.isPersonTaxable(person):
                    if tax.attributes["tax_type"] == "flat":
                        flat_tax += tax.attributes["tax_amount"]
                    elif tax.attributes["tax_type"] == "prop":
                        prop_tax += tax.attributes["tax_amount"]
                    else:
                        print("error: no such tax type")
                        
            person.taxes["flat"],person.taxes["prop"] = flat_tax, prop_tax
            
                
                
    def consume(self):
        for person in self.people:
            person.consumeGoods()
            
    def returnPeopleStats(self,key,aggregate_operation):
        vec = []
        for person in self.people:
            attrs = person.attributes
            resources = person.resources
            taxes = person.taxes
            instances = person.instances
            
            combined_dict = {**attrs,**resources,**taxes,**instances}
            
            to_append = combined_dict[key]
            vec.append(to_append)
            
        if aggregate_operation == "none":
            pass
        elif aggregate_operation == 'mean':
            vec = np.mean(vec)
        elif aggregate_operation == 'sum':
            vec = np.sum(vec)
        elif aggregate_operation == "unique":
            vec = np.unique(vec)
        else:
            print("error: aggregate_operation not recognized")
        return vec
    
    def nextTick(self):
        self.updatePeoplesTaxes()
        self.work()
        self.taxPeople()
        self.consume()
        self.updateJobs()
        

g1 = Game()
t1 = Tax(["culture","name"],[[0,2],"Ted"],["=","="],"xtax","money","flat",2)
t2 = Tax(["culture","name"],[[0,2],"Ted"],["=","="],"xtax","money","prop",.1)
g1.taxes.append(t1)
g1.taxes.append(t2)
g1.nextTick()