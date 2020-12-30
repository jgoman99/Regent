# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 21:19:10 2020

@author: jgfri
"""

from scipy import optimize
import numpy as np

import datetime

start = datetime.datetime.now()

tax = Tax(["culture","name"],[[0,2],"Ted"],["=","="],"xtax","money","flat",2)
people = [Person() for i in range(1000)]
for person in people:
    tax.isPersonTaxable(person)
    





end = datetime.datetime.now()
print(end - start)