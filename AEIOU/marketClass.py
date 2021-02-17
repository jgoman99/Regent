# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 01:32:21 2021

@author: jgfri
"""

from cvxopt.glpk import ilp
import numpy as np
from cvxopt import matrix


def market(supply,bids=[1,2,3,4,5,6]):
    m = len(bids)
    c= matrix(np.array(bids, dtype= float))
    c = -c
    coeff= np.array([np.ones(m, dtype=float)])
    G=matrix(coeff)
    h=matrix(1*np.array([supply], dtype = float))
    I=set()
    B=set(range(m))
    (status,x)=ilp(c,G,h,matrix(1., (0,m)),matrix(1., (0,1)),I,B)
    
    return(x)
    
