# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 22:30:41 2021

@author: jgfri
"""
import random as rd
import math
year = 902

class Technology:
    def __init__(self,num_id):
        self.id = "tech" + str(num_id)
        self.power = 1.00
        self.applications = {'Person':{'health': .05}}
        
        

class Person:
    def __init__(self):
        self.age = None
        self.job = None
        self.culture = None
        self.religion = None
        self.health = None
        
    def getOlder(self, tech):
        pass

class Planet:
    def __init__(self):
        self.countries = [Country("country" + str(i)) for i in range(5)]
        self.setUpCountryRelations("randomize")
        self.news = []
        self.history = []
        
    def setUpCountryRelations(self, specialRule = "randomize"):
        for i in range(len(self.countries)-1):
            for j in range(i+1,len(self.countries)):
                meetEntity(self.countries[i],self.countries[j])
                
    def decideCountriesActions(self):
        for country in self.countries:
            countryAction = decideCountryAction(country, self)
            if countryAction != "":
                self.news.extend(countryAction)
                
    def fightWars(self):
        for country in self.countries:
            for otherCountry,opinion in country.relations.items():
                if opinion == "war":
                    otherEntity = getEntityFromId(otherCountry, self)
                    battle_type, kills_army1, kills_army2 = fightBattle(country,otherEntity)
                    # this tooltip is sometimes wrong
                    self.news.append(battle_type + " fought between " +
                                     country.id + " and " + otherCountry + ". " + str(kills_army2) +
                                     " and " + str(kills_army1) + " soldiers dead respectively.")
                
    def nextTick(self):
        self.news = []
        self.decideCountriesActions()
        self.fightWars()
        if self.news != []:
            self.history.append(self.news)
    
class Country:
    def __init__(self, id_num):
        self.id = id_num
        self.population = rd.randint(1000,25000)
        self.army = math.floor(rd.uniform(.005, .02)*self.population)
        self.money = rd.randint(50,1000)
        self.opinions = {}
        self.relations = {}
        self.warExhaustion = 0
        self.warThreshold = .2
    
def coinflip(prob):
    return rd.random() < prob

def annexCountry(entity1,entity2,planet):
    entity1.population += entity2.population
    entity1.money += entity2.money
    
    entity2_id = entity2.id
    for country in planet.countries:
        country.opinions.pop(entity2_id, None)
        country.relations.pop(entity2_id, None)
    planet.countries.remove(entity2)
    
    
    
    

# Note: countries will fight two battles a turn at min. (one on as turn, one on bs turn)
def fightBattle(entity1,entity2):
    # first rolls for type of engagement. < 6 is a minor skirmish. 6-9 is a battle, 10 is a major battle
    battle_type_roll = rd.randint(0, 10)
    army1 = entity1.army
    army2 = entity2.army
    if battle_type_roll < 6:
        battle_type = "skirmish"
        army_1_width,army_2_width = rd.uniform(0.025,.075),rd.uniform(0.025,.075)
    elif battle_type_roll < 10:
        battle_type = "battle"
        army_1_width,army_2_width = rd.uniform(0.075,.15),rd.uniform(0.075,.15)
    else:
        battle_type = "campaign"
        army_1_width,army_2_width = rd.uniform(0.15,.25),rd.uniform(0.15,.25)
        
    eff_army1 = math.floor(army1*army_1_width)
    eff_army2 = math.floor(army2*army_2_width)
    
    tactics_army1 = rd.uniform(.33, .66)
    tactics_army2 = rd.uniform(.33, .66)
    
    kills_army1 = sum([coinflip(tactics_army1) for i in range(eff_army1)])
    kills_army2 = sum([coinflip(tactics_army2) for i in range(eff_army2)])
    
    entity1.army -= kills_army2
    entity2.army -= kills_army1
    
    changeWarExhaustion(entity1, kills_army2/entity1.army)
    changeWarExhaustion(entity2, kills_army1/entity2.army)
    
    return battle_type, kills_army1, kills_army2
        
    
    
def changeWarExhaustion(entity1, modifier):
    entity1.warExhaustion += modifier
    
    if entity1.warExhaustion < 0:
        entity1.warExhaustion = 0
        
# remember ! war is currently based on first match
def decideCountryAction(entity1,planet):
    countryAction = []
    relations =  dict(filter(lambda item: "country" in item[0],
                                   entity1.relations.items()
                                   ))
    wars = dict(filter(lambda item: 'war' in item[1], relations.items()))
    for war in wars:
            we1, wt1 = entity1.warExhaustion, entity1.warThreshold
            entity2 = getEntityFromId(war,planet)
            we2, wt2 = entity2.warExhaustion, entity2.warThreshold
            army1, army2 = entity1.army, entity2.army
            
            tempAction1 = ''
            if army1 <= 0:
                annexCountry(entity2, entity1, planet)
                tempAction1 = str(entity2.id) + " annexed " + str(entity1.id)
            elif army2 <= 0:
                annexCountry(entity1, entity2, planet)
                tempAction1 = str(entity1.id) + " annexed " + str(entity2.id)
            if (we1 > wt1) & (we2 > wt2):
                changeRelation(entity1, entity2, "peace")
                tempAction1 = str(entity1.id) + " made peace with " + str(entity2.id)

            if tempAction1 != '':
                countryAction.append(tempAction1)
    
    if ('war' not in relations) & (entity1.warExhaustion == 0):
        war_target = checkWarTargets(entity1, planet)
        if war_target != "":
            changeRelation(entity1,war_target,"war")
            countryAction.append(str(entity1.id) + " declared war on " + str(war_target.id))
    
    
    
    
    
    return countryAction
        
def getEntityFromId(id_str,planet):
    return planet.countries[[i.id for i in planet.countries].index(id_str)]

            
def checkWarTargets(entity1,planet):
    opinions = dict(filter(lambda item: "country" in item[0],
                                   entity1.opinions.items()))
    possible_war_targets = []
    for opinion in opinions:
        if opinions[opinion] < -25:
            possible_war_targets.append(opinion)
    war_targets = []
    for possible_war_target in possible_war_targets:
        possible_war_target_entity = getEntityFromId(possible_war_target,planet)
        if entity1.army > 1.5*(possible_war_target_entity.army):
            war_targets.append(possible_war_target_entity)
            
    if (len(war_targets) > 0):
        return war_targets[0]
    else:
        return ""
    
def changeOpinion(entity1,entity2, modifier, mutual = False):
    if mutual:
        entity1.opinions[entity2.id] += modifier
        entity2.opinions[entity1.id] += modifier
    else:
        entity1.opinions[entity2.id] += modifier
        
    if entity1.opinions[entity2.id] < -100:
        entity1.opinions[entity2.id]  = -100
    elif entity1.opinions[entity2.id] > 100:
        entity1.opinions[entity2.id]  = 100
        
    if entity2.opinions[entity1.id] < -100:
        entity2.opinions[entity1.id]  = -100
    elif entity2.opinions[entity1.id] > 100:
        entity2.opinions[entity1.id]  = 100
    
    
def changeRelation(entity1,entity2,new_relation):
        entity1.relations[entity2.id] = new_relation
        entity2.relations[entity1.id] = new_relation
        
        if new_relation == 'war':
            changeOpinion(entity1, entity2, -25, mutual = True)
        elif new_relation == 'peace':
            changeOpinion(entity1, entity2, 15, mutual = True)
            
        
def knowEntity(entity1,entity2):
    if entity2.id in entity1.opinions.keys():
        return True
    else:
        return False
    
def meetEntity(entity1,entity2, specialRule = "none"):
    if not knowEntity(entity1, entity2) & (specialRule == "randomize"):
        ranNum = rd.randint(-50, 50)
        entity1.opinions[entity2.id] = ranNum
        entity2.opinions[entity1.id] = ranNum
    elif not knowEntity(entity1, entity2):
        entity1.opinions[entity2.id] = 0
        entity2.opinions[entity1.id] = 0
        
p1 = Planet()
p1.setUpCountryRelations()
p1.nextTick()
    