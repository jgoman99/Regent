# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 22:20:33 2021

@author: jgfri
"""
import numpy as np
import random as rd
import itertools

class Game:
    def __init__(self,size = 3):
        self.map = np.matrix('1 3 2; 2 1 3; 3 2 1')
        self.solution = np.copy(self.map)
        self.size = size
        
        for i in range(self.size*2):
            removeOne(self.map)
        
    
        

    

    
    #lame brute force method.
def tryToSolve(sudoku_map):
    
    s_map = np.copy(sudoku_map)
    zeroes_list = np.where(s_map==0)
    x,y = zeroes_list
    x,y = x.tolist(),y.tolist()
    
    combos = [p for p in itertools.product(range(1,s_map.size + 1), repeat=len(x))]
    
    num_solutions = 0
    for combo in combos:
        for item in combo:
            s_map[x,y] = item
        
        
        if checkSolution(s_map):
            num_solutions += 1
            
    if num_solutions == 1:
        return True
    else:
        return False
                
# not implemented yet
def createSudokuPuzzle():
    pass           
            
        

        
def checkSolution(sudoku_map):
    # Checks rows
    for i in range(sudoku_map.size):
        zed = np.unique(sudoku_map[i].tolist())
        zed = zed[zed!=0]
        if zed.shape[0] != sudoku_map.size:
            return False
    # Checks columns
    for i in range(sudoku_map.size):
        zed = np.unique(sudoku_map[i].tolist())
        zed = zed[zed!=0]
        if zed.shape[0] != sudoku_map.size:
            return False
        
    return True
        
def removeOne(sudoku_map):
    old_map = np.copy(sudoku_map)
    x,y = rd.randint(0,sudoku_map.shape[0]-1), rd.randint(0,sudoku_map.shape[0]-1)
    
    sudoku_map[x,y] = 0
    if tryToSolve(sudoku_map):
        old_map = np.copy(sudoku_map)
        
    return old_map
