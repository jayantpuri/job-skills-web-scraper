# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 00:32:10 2021

@author: slayer
"""

import json
import re
import math
from collections import Counter


s=""
s2=""
new_set = []
new_set2=[]
second_set=[]
second_set2=[]
final_set=[]
final_set2=[]
skills = {}
skills2={}


with open("dat.json", "r") as first:
   s = first.readlines()
   

for skill in s[0].split(","):
         
      skill = skill.replace("[", "")
      skill = skill.replace("]", "")
      new_set.append(skill)
        
for skill in new_set:
    skill = skill.replace("(", "")
    skill = skill.replace(")", "")
    second_set.append(skill)    

for skill in second_set:
    skill = re.sub('[^A-Za-z0-9]', ' ', skill)
    skill = re.sub(r'[^\w\s]','', skill)
    skill= skill.strip()
    final_set.append(skill)
    


with open("data_analyst.json", "r") as second:
   s2 = second.readlines()
   

for skill in s2[0].split(","):
         
      skill = skill.replace("[", "")
      skill = skill.replace("]", "")
      new_set2.append(skill)
        
for skill in new_set2:
    skill = skill.replace("(", "")
    skill = skill.replace(")", "")
    second_set2.append(skill)    

for skill in second_set2:
    skill = re.sub('[^A-Za-z0-9]', ' ', skill)
    skill = re.sub(r'[^\w\s]','', skill)
    skill= skill.strip()
    final_set2.append(skill)

counterA = Counter(final_set)
counterB = Counter(final_set2)

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

print(counterA)
print(counterB)

print("Similarity score: "+ str(counter_cosine_similarity(counterA,counterB)))

