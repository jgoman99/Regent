# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 20:23:59 2021

@author: jgfri
"""
import re
import numpy as np
import json 


class Game:
    def __init__(self):
        self.descriptions =  {"economyDesc": "good", "weatherDesc": "bad","playerCulture": "blue"}
        self.storyNodes = readStoryNodesFromText()
        self.currentStoryNode = self.storyNodes[0]
        
    def displayCurrentStoryNode(self):
        node = self.currentStoryNode 
        print(u"eventId: ", node.eventId, "): ",node.desc)
        
        options = node.options
        options = returnOptions(node,self)
             
        for idx, option in enumerate(options):
            print(u"",idx,":"," ",option["desc"])
            
    #note: technically you could call any event here, but in a gui only valid options will be available.         
    def chooseBranch(self,option):
        nextStoryNodeId = str(chooseOption(option,self))
        newStoryNodeLoc = [node.eventId == nextStoryNodeId for node in self.storyNodes]
        self.currentStoryNode=np.array(self.storyNodes)[np.where(newStoryNodeLoc)][0]
        
    def chooseBranchByNumber(self,num):
        node = self.currentStoryNode 
        options = returnOptions(node,self)
        if num < len(options):
            option = options[num]
            self.chooseBranch(option)
        else:
            print("Out of bounds number")
            
    def playGame(self):
        while True:
            self.displayCurrentStoryNode()
            action_input = input('Action: ')
            if action_input == "end":
                break
            else:
                self.chooseBranchByNumber(int(action_input))
        
        
def read_dialogue_string(diag_string,game):
    variables =[x for x in re.finditer(r"([$])(?:(?=(\\?))\2.)*?\1",diag_string)]
    variable_names = [variable.group() for variable in variables]
    variable_names_cleaned = [re.sub("\$","",variable) for variable in variable_names]
    variable_values = [game.descriptions[variable_name] for variable_name in variable_names_cleaned]
    
    diag_string_with_variables = diag_string
    for idx,variable in enumerate(variable_names_cleaned):
        value = variable_values[idx]
        diag_string_with_variables = re.sub(variable,value,diag_string_with_variables)
        
    
    return diag_string_with_variables

def checkRequirements(option,game):
    requirements = option["requirements"]
    meets_requirements = []
    # if requirements = [] returns true. Option for if no requirements needed
    if requirements == []:
        return(True)
    
    for requirement in requirements:
        meets_requirements.append(checkRequirement(requirement,game))
    
    if False in meets_requirements:
        return(False)
    else:
        return(True)

def checkRequirement(requirement,game):
    var1 = requirement[0]
    sign = requirement[1]
    value = requirement[2]
    
    validRequirement = False
    if sign == "=":
        if game.descriptions[var1] == value:
            validRequirement = True
    elif sign == "!=":
        if game.descriptions[var1] != value:
            validRequirement = True
    else:
        raise Exception("Requirement sign not found")
        
    return(validRequirement)

def performEffect(effect,game):
    var1 = effect[0]
    sign = effect[1]
    value = effect[2]
    if sign == "=":
        game.descriptions[var1] = value
    elif sign == "+":
        game.descriptions[var1] += value
    elif sign == "-":
        game.descriptions[var1] -= value
    else:
        raise Exception("Sign not found")
        
def returnOptions(storyNode,game):
    options = storyNode.options
    valid_options = []
    for option in options:
        valid_options.append(checkRequirements(option, game))
        
    valid_options = np.array(options)[np.where(valid_options)]
    return(valid_options)
    
def chooseOption(option,game):
    effects = option["effects"]
    for effect in effects:
        performEffect(effect,game)
    return(option["nextEvent"])

class storyNode:
    def __init__(self,eventId,desc,options):
        self.eventId = eventId
        self.desc = desc
        self.options = options
        
        
def readStoryNodesFromText(path="./storynodes/storynodes.txt"):
    text_lines = []
    with open("./storynodes/storynodes.txt", 'r') as reader:
        for line in reader:
            line = line.rstrip('\n')
            line = re.sub(r"\'","",line)
            line = re.sub(r"'","",line)
            text_lines.append(line)
        
    node_boundaries = np.where([text_line == "" for text_line in text_lines])[0]
    nodes = []
    start = 0 
    for node_boundary in node_boundaries:
        nodes.append(text_lines[start:node_boundary])
        start = node_boundary + 1
    nodes.append(text_lines[start:len(text_lines)])
    
    # note: add error warnings here fpr mult of same id
    storyNode_list = []
    for node in nodes:
        eventId = ""
        desc = ""
        options = []
        for line in node:
            tag = re.match(r"^[^:]*",line)
            rest_of_line = line[tag.end()+2:len(line)]
            if tag.group() == "eventId":
                eventId = rest_of_line
            elif tag.group() == "desc":
                desc = rest_of_line
            elif tag.group() == "option":
                options_dict = json.loads(rest_of_line)
                options.append(options_dict)
            
        newStoryNode = storyNode(eventId, desc, options)
        storyNode_list.append(newStoryNode)
    
    return(storyNode_list)
        

game = Game()
game.playGame()
