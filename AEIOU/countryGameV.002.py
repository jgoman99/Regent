# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 00:45:16 2021

@author: jgfri
"""
import marketClass
import random as rd
import numpy as np
import time as time
import math


#fix bug in this version that is destroying money

class Country():
    def __init__(self):
        self.towns = [Town() for i in range(10)]
        self.resources = {"food":0,"luxury":0}
        self.government_prices = {"food":1, "luxury": 1}
        self.money = 100000
        
    def nextTick(self):
        for town in self.towns:
            town.nextTick(self)
            
    def returnStats(self):
        for town in self.towns:
            town.returnStats()

class Town():
    def __init__(self):
        self.people = [Person() for i in range(rd.randint(300, 1000))]
        self.prices = {"food" : 1, "luxury": 1}
        
    # note higher in order goes first. should change?
    def marketForGood(self,good,bidders,country):
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
            
            if num_goods > amount_demanded:
                num_goods -= amount_demanded
                supplier.money += amount_demanded*min_price
                amount_demanded = 0
                supplier.goods[good] -= amount_demanded
            
            if num_goods > 1:
                supplier.money += num_goods*country.government_prices[good]
                country.money -= num_goods*country.government_prices[good]
                country.resources[good] += num_goods
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
    
    def nextTick(self,country):
        self.workJobs()
        
        bidders = self.people
        self.prices["food"], bidders = self.marketForGood("food",bidders,country)
        self.prices["luxury"], bidders = self.marketForGood("luxury",bidders,country)
        self.consumeGoodsAll()
        
    #  statistics:
    def returnStats(self):
        print(u"population:", len(self.people))
        print(u"prices:", self.prices)
        total_money = sum([person.money for person in self.people])
        print(u"money:", total_money)


class Person:
    def __init__(self):
        self.health = 0
        self.healthGenerator()
        self.content = 80
        self.money = rd.randint(10,100)
        self.goods = {"food": 0,"luxury":0}
        self.isDeadbool = False
        self.isDiscontentBool = False
        self.job = self.jobGenerator()
        
        self.attributes = {"culture": rd.randint(0,2),"religion": rd.randint(0, 2)}
        
    def workJob(self):
        if self.job == "farmer":
            self.goods["food"] += round(rd.uniform(0,1.5)*(1+self.health/100))
        elif self.job == "artisan":
            self.goods["luxury"] += round(rd.uniform(0,1)*(1+self.health/100))
            
            
    # this can probably be speed up using np.random.normal(75,15,1000)
    def healthGenerator(self):
        change = int(np.random.normal(75,15,1))
        self.updateHealth(change)
        
    def jobGenerator(self):
        roll = rd.randint(0,100)
        if roll > 30:
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
            self.updateHealth(-2)
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
for i in range(1):
    print(c1.returnStats())
    c1.nextTick()
    print(c1.returnStats())
    
