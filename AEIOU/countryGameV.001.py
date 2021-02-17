# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 00:45:16 2021

@author: jgfri
"""
import marketClass
import random as rd
import numpy as np
import time as time

class Country():
    def __init__(self):
        self.people = [Person() for i in range(1000)]
        self.prices = {"food" : 1, "luxury": 1}
        
    # note higher in order goes first. should change?
    def marketForGood(self,good,bidders):
        bidders = np.array(bidders)
        suppliers = np.array(self.people)
        
        bid_vec = np.array([i.money for i in bidders])
        supply_vec = [i.goods[good] for i in suppliers]
        amount_supplied = sum(supply_vec)
        results = marketClass.market(amount_supplied,bid_vec)
        
        winnerBool = [i == 1 for i in results]
        winners = np.array(bidders)[winnerBool]
        min_price = min(bid_vec[winnerBool])
        #print(u"min price: ", min_price)
        
        amount_demanded = sum(winnerBool)
        for supplier in suppliers:
            num_goods = supplier.goods[good]
            if amount_demanded < 1:
                break
            
            if num_goods > amount_demanded:
                num_goods = amount_demanded
                
            supplier.money += num_goods*min_price
            amount_demanded -= num_goods
            supplier.goods[good] = 0
            
        for winner in winners:
            winner.money -= min_price
            winner.goods[good] += 1
            
        return (min_price,winners)
            
        
        

        
    
    def workJobs(self):
        for person in self.people:
            person.workJob()
            
    def consumeGoodsAll(self):
        for person in self.people:
            person.consumeGoods()
    
    def nextTick(self):
        self.workJobs()
        
        bidders = self.people
        self.prices["food"], bidders = self.marketForGood("food",bidders)
        self.prices["luxury"], bidders = self.marketForGood("luxury",bidders)
        self.consumeGoodsAll()


class Person:
    def __init__(self):
        self.health = 80
        self.content = 80
        self.money = rd.randint(10,100)
        self.goods = {"food": 0,"luxury":0}
        self.isDeadbool = False
        self.isDiscontentBool = False
        self.job = self.jobGenerator()
        self.sales = {}
        
    def workJob(self):
        if self.job == "farmer":
            self.goods["food"] += rd.randint(0,2)#*(self.health/100)
        elif self.job == "artisan":
            self.goods["luxury"] += rd.randint(0,1)#*(self.health/100)
            
            
    def jobGenerator(self):
        roll = rd.randint(0,100)
        if roll > 5:
            return("farmer")
        else:
            return("artisan")
    
    def consumeGoods(self):
        content = -1
        if self.goods["food"] >= 1:
            self.goods["food"] -= 1
            self.updateHealth(1)
            content += 1
        else:
            self.updateHealth(-1)
            content -= 2
            
        if self.goods["luxury"] >= 1:
            self.goods["luxury"] -= 1
            content += 1
        else:
            pass
        
        self.updateContent(content)
            
    def updateHealth(self,health_change):
        self.health += health_change
        
        if self.health > 100:
            self.health = 100
        elif self.health <= 0:
            self.isDeadbool = True
            
    def updateContent(self,change):
        self.content += change
        
        if self.content > 100:
            self.content = 100
        elif self.content <= 0:
            self.isDiscontentBool = True
            self.content = 0
            
        
        
# run som stuff
c1 = Country()
print(sum([i.money for i in c1.people]))
for i in range(1):
    c1.nextTick()
    print(c1.prices)
print(sum([i.money for i in c1.people]))