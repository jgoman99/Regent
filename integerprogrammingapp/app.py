# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 16:50:37 2021

@author: jgfri
"""

from cvxopt.glpk import ilp
import numpy as np
from cvxopt import matrix
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import re



class stackedExample(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        
        self.constraintEdits = []
        self.lay = QHBoxLayout(self)
        self.leftLay = QVBoxLayout(self)
        self.rightLay = QVBoxLayout(self)
        self.formulaStr = ""
        self.formula = None
        self.constraintMat = np.matrix([])
        self.constraintStr = ""
        self.vars = []
        
        formulaLabel = QLabel("Formula:")
        self.formulaEdit = QLineEdit("+ x1 + 2x2 + x3")
        first_lay = QHBoxLayout()
        first_lay.addWidget(formulaLabel)
        first_lay.addWidget(self.formulaEdit)
        
        formulaOutputLay = QVBoxLayout()
        self.formulaOutputLabel = QLabel("")
        formulaOutputLay.addWidget(self.formulaOutputLabel)
        
        second_lay = QHBoxLayout()
        constraintsLabel = QLabel("Constraints:")
        addConstraintsButton = QPushButton("Add Constraint")
        removeConstraintsButton = QPushButton("Remove Constraint")
        second_lay.addWidget(constraintsLabel)
        second_lay.addWidget(addConstraintsButton)
        second_lay.addWidget(removeConstraintsButton)
        
        self.third_lay = QVBoxLayout()

        fourth_lay = QHBoxLayout()
        calculateButton = QPushButton("Calculate")
        fourth_lay.addWidget(calculateButton)
        
        self.constraintOutputLay = QVBoxLayout()
        self.constraintOutputLabel = QLabel("")
        self.constraintOutputLay.addWidget(self.constraintOutputLabel)
        
        self.leftLay.addLayout(first_lay)
        self.leftLay.addLayout(formulaOutputLay)
        self.leftLay.addLayout(second_lay)
        self.leftLay.addLayout(self.third_lay)
        self.leftLay.addLayout(fourth_lay)
        self.leftLay.addLayout(self.constraintOutputLay)
        

        
        
        self.lay.addLayout(self.leftLay)
        self.lay.addLayout(self.rightLay)
        
        addConstraintsButton.clicked.connect(self.addConstraint)
        removeConstraintsButton.clicked.connect(self.removeConstraint)
        calculateButton.clicked.connect(self.calculate)

    def addConstraint(self):
        newEdit = QLineEdit("")
        self.constraintEdits.append(newEdit)
        self.refresh()
        
    def removeConstraint(self):
        pass
        # self.third_lay.removeWidget(self.constraintEdits[0])
        # self.constraintEdits.pop()
        # self.refresh()
        
    def refresh(self):
        temp_arr_con = []
        for constraintEdit in self.constraintEdits:
            temp_arr_con.append(constraintEdit.text())
            self.third_lay.addWidget(constraintEdit)
            constraintEdit.show()
        self.constraintStr = str(temp_arr_con)
        print(self.constraintStr)

        
        self.calculateNumVariables()
        self.formula = convertStrToArray(self.formulaStr,self.vars)
        self.formulaOutputLabel.setText(str(self.formula))
        
        
        new_arr = []
        self.constraintStr = []
        for constraintEdit in self.constraintEdits:
            temp_arr = convertStrToArray(constraintEdit.text(), self.vars)
            if new_arr == []:
                new_arr = temp_arr
            else:
                new_arr.append(temp_arr)
        self.constraintMat = -np.matrix(np.array(new_arr))
        self.constraintOutputLabel.setText(self.constraintMat)
    
            
    def calculate(self):
        self.formulaStr = self.formulaEdit.text()
        self.refresh()
        
    def calculateNumVariables(self):
        allstr = self.formulaStr + str(self.constraintStr)
        allstr = allstr.replace(";"," ")
        allstr = allstr.replace("+"," ")
        allstr = allstr.replace("-"," ")
        allvars = allstr.split()
        self.vars = set(allvars)
        
def convertStrToArray(string, all_vars):
    zeroBool = False
    if "x0" in all_vars:
        zeroBool = True
        
    idxs = [m.start() for m in re.finditer('\+', string)]
    idxs.append(len(string))
    
    cleaned_vars = []
    for i in range(len(idxs)-1):
        start = idxs[i]
        end = idxs[i+1]
        cleaned_vars.append(string[start:end])
        
    signs = []
    for i in range(len(cleaned_vars)):        
        if cleaned_vars[i].find("+") != -1:
            signs.append("+")
        else:
            signs.append("-")
    
    cleaned_vars = [cleaned_var.replace("+"," ") for cleaned_var in cleaned_vars]
    cleaned_vars = [cleaned_var.replace(" ","") for cleaned_var in cleaned_vars]
    
    a = []
    var_id = []
    for i in range(len(cleaned_vars)):   
        cleaned_var = cleaned_vars[i]
        end = re.search("x",cleaned_var).end()
        
        temp_a = cleaned_var[0:(end-1)]
        
        if temp_a == '':
            temp_a = '1'
            
        var_id.append(cleaned_var[end:len(cleaned_var)])
        a.append(temp_a)
        
    if not zeroBool:
        var_id = [str(int(i) - 1) for i in var_id]
        
    array = np.zeros(len(all_vars))
    for i in range(len(signs)):
        idx = var_id[i]
        array[int(idx)] = int(signs[i] + a[i])
        
    return array
        

    
    
        
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = stackedExample()
    w.show()
    sys.exit(app.exec_())


c=matrix(np.ones(6,dtype=float))
coeff=np.array([[1,1,0,0,0,0],
                [1,1,0,0,0,1],
                [0,0,1,1,0,0],
                [0,0,1,1,1,0],
                [0,0,0,1,1,1],
                [0,1,0,0,1,1]
                ],dtype=float)
G=matrix(-coeff)
h=matrix(-1*np.ones(6))
I=set([2,3,4,5])
B=set([0,1])
(status,x)=ilp(c,G,h,matrix(1., (0,6)),matrix(1., (0,1)),I,B)
