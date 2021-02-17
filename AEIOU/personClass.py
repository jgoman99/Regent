# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 23:32:07 2021

@author: jgfri
"""
#imports
from scipy.stats import binom
import numpy as np

# Global Vars (Move these later)
deathChance = 300000000
agePenalty = 4

class Person:
    def __init__(self):
        self.ageInt = 18
        self.isAliveBool = True
    
    
def ageOneYear(person):
    age = person.ageInt
    prob = (age**agePenalty)/deathChance
    flip = binom.rvs(1, prob, size=1)
    
    if flip == 1:
        person.isAliveBool = False
    else:
        person.age += 1
        

#unvectorized, slow, so may need rewrite
def checkMeanAge():
    length = 1000
    age_list = [0]*length
    for i in range(length):
        age = 0
        while True:
            prob = (age**agePenalty)/deathChance
            flip = binom.rvs(1, prob, size=1)
            if flip == 1:
                age_list[i] = age
                break
            else:
                age += 1
        
    return(np.mean(age_list))
        
    