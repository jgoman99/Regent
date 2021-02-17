# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 00:45:16 2021

@author: jgfri
"""
import marketClass
import random as rd
import numpy as np

class Country:
    def __init__(self):
        self.people = [Person() for i in range(1000)]
        self.prices = {"food": 1}
        
    def marketDay(self):
        bids = [i.money for i in self.people]
        supply = sum([i.goods["food"] for i in self.people])
        results = marketClass.market(supply,bids)
        winners = [i == 1 for i in results]
        bids = np.array(bids)
        min_price = min(bids[winners])
        
        winner_array = np.array(self.people)[winners]
        for person in winner_array:
            person.money -= min_price
            person.goods["food"] += 1
        
        print(min_price)
        return(winners)
    
    def workJobs(self):
        for person in self.people:
            person.workJob()
            
    def consumeGoodsAll(self):
        for person in self.people:
            person.consumeGoods()
    
    def nextTick(self):
        self.workJobs()
        self.marketDay()
        self.consumeGoodsAll()


class Person:
    def __init__(self):
        self.health = 80
        self.money = rd.randint(1,4)
        self.goods = {"food": 0}
        self.isDeadbool = False
        self.job = "farmer"
        self.sales = {}
        
    def workJob(self):
        if self.job == "farmer":
            self.goods["food"] += rd.randint(0,1)
            
    
    def consumeGoods(self):
        if self.goods["food"] >= 1:
            self.goods["food"] -= 1
            self.updateHealth(5)
        else:
            self.updateHealth(-10)
            
    def updateHealth(self,health_change):
        self.health += health_change
        
        if self.health > 100:
            self.health = 100
        elif self.health <= 0:
            self.isDeadbool = True
        
        
# run som stuff
c1 = Country()
c1.nextTick()