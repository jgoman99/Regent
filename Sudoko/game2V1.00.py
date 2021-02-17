
#probably this will become both solver, and creator
# possibly may be error due to -0. probs not
# good chance I accidentally doubled min/max constraints..Should check
from cvxopt.glpk import ilp
import numpy as np
from cvxopt import matrix

def createSudokuPuzzle(size=2):
    # Arbitrary function, since only constraints matter
    c = matrix(np.ones(size**2,dtype=float))
    # Changes to maximization function.
    c = -c
    # sets up row constraints
    row_array = np.array([])
    for i in range(size):                        
        new_constraint = np.array(0*np.ones(size**2))
        new_constraint[i*size:i*size+size] = 1
        new_constraint = [new_constraint]
        if i == 0:
            row_array = new_constraint
        else:
            row_array = np.append(row_array,new_constraint,axis=0)
    
    # sets up col constraints
    col_array = np.array([])
    for i in range(size):                        
        new_constraint = np.array(0*np.ones(size**2))
        for j in range(size):   
            new_constraint[i+size*j] = 1
        new_constraint = [new_constraint]
        if i == 0:
            col_array = new_constraint
        else:
            col_array = np.append(col_array,new_constraint,axis=0)
            
    # sets up variable max constraints
    variables_array = np.array([])
    for i in range(size**2):
        new_constraint = np.array(0*np.ones(size**2))
        new_constraint[i] = 1
        new_constraint = [new_constraint]
        if i == 0:
            variables_array = new_constraint
        else:
            variables_array = np.append(variables_array,new_constraint, axis =0)
    # sets up variable min constraints
    for i in range(size**2):
        new_constraint = np.array(0*np.ones(size**2))
        new_constraint[i] = 1
        new_constraint = [-new_constraint]
        variables_array = np.append(variables_array,new_constraint, axis =0)
        
    # makes sure variables in a row can share same values
    # note: THere must be second part of script so that x1 isn't always largest, etc
    unique_constraint = np.array([])
    for i in range(size):
        idx = 3*i
        for j in range(0,size):
            new_constraint = np.array(0*np.ones(size**2))
            new_constraint[idx] = 1
            for k in range(j+1,size):
                add_constraint = np.copy(new_constraint)
                add_constraint[idx+k] = -1
                add_constraint = [add_constraint]
                if len(unique_constraint):
                    unique_constraint = [add_constraint]
                else:
                    unique_constraint = np.append(unique_constraint,[add_constraint],axis=0)
                    

                
                
        
    # now we combine into our constraint matrix
    coeff = np.append(row_array,col_array,axis = 0)
    coeff = np.append(coeff, variables_array, axis = 0)
    G=matrix(coeff)
    
    # This is the right hand side of the equation
    #mx1 dense 'd' matrix
    sum_values = sum(range(size+1)) 
    row_col_constraints = np.array([sum_values*np.ones(size*2)])
    # might have made an error here
    max_constraints = np.array([3*np.ones(size**2)])
    min_constraints = np.array([-1*np.ones(size**2)])
    h = np.append(row_col_constraints,max_constraints)
    h = np.append(h,min_constraints)
    h= matrix(h)
    
    # pxn dense or sparse 'd' matrix with p>=0
    A= matrix(1., (0,size**2))
    # px1 dense 'd' matrix
    b = matrix(1., (0,1))
    
    # set with indices of integer variables
    I=set(range(size**2))
    # set with indices of binary variables
    B=set()
    
    (status,x)=ilp(c,G,h,A,b,I,B)
    return((status,np.array(x).reshape(size,size)))
    
    
    