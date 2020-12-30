# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 21:19:10 2020

@author: jgfri
"""

from scipy import optimize
import numpy as np

import datetime

start = datetime.datetime.now()

people = [Person() for i in range(100)]
for person in people:
    person.allocateTime()
end = datetime.datetime.now()
print(end - start)
print(result.x)