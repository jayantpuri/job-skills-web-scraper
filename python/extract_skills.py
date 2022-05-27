# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 21:50:46 2021

@author: slayer
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from bs4 import BeautifulSoup, NavigableString, Tag
import requests
from random import random
from time import sleep
from email.message import EmailMessage
from collections import namedtuple
import smtplib
import csv
import numpy as np
import json

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
list_stop = []

list_lemmatize = []
global no_jobs 

skill_phrase = ["skills", "requirements", "experience", "qualifications", "responsibilities", "what we are looking for", "what you bring"]

headers={}


def generate_url(job_title, job_location, page):
    headers = {"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
    url_template = "https://www.indeed.com/jobs?q={}&l={}&start={}"
    url = url_template.format(job_title, job_location, page)
    return url

def unique(un):
    x = np.array(un)
    return np.unique(x)


def record(job):
    pos_tag=[]
    tokens=[]
    list_skill =[]
    list_lemmatize = []
    c= [] 
    count=0
    anchor = job.parent
    link = anchor.get('href')
    
    link = "https://www.indeed.com"+link

    u1 = requests.get(link)   
    l = BeautifulSoup(u1.content, 'html.parser')   
    ind_card = l.find(id = 'jobDescriptionText')
    
    try:
        if len(ind_card.contents)==1:
            for item in ind_card.contents[0].contents:
                c.append(item)
                
        elif len(ind_card.contents)>1:
             for item in ind_card.contents:
                c.append(item)
    except AttributeError:
        c.append(" ")
        
            
    def check_skill(count):
        while count< len(c):
            if "<ul>" in str(c[count]):
                if str(c[count]) not in list_skill:
                    list_skill.append(str(c[count]))
                    break
            count=count+1
            
    while count < len(c):
        if isinstance(c[count], Tag):
            banner = c[count] 
            for skill in skill_phrase:
                if skill.casefold() in banner.text.casefold():
                    check_skill(count+1)
            
        count= count+1
     
    # Extracting tokens freom the list of skills
    for item in list_skill:
        item = item.replace("<ul>", " ")
        item = item.replace("</ul>", " ")
        item = item.replace("<li>", " ")
        item = item.replace("<b>", " ")
        item = item.replace("</b>", " ")
        item = item.replace("\n", " ")
        item= item.replace("<i>", " ")
        item= item.replace("</i>", " ")
        item= item.split("</li>")
        for sentence in item:
            tokens = tokens+word_tokenize(sentence)
    
    for skill in tokens:
        list_lemmatize.append(lemmatizer.lemmatize(skill))
        
    pos_tagged = nltk.pos_tag(list_lemmatize) 

    for word in pos_tagged:
        if word[1] =="NN" or word[1] =="NNP":
           i = pos_tagged.index(word)
           pos_tag.append( pos_tagged[i-1][0]+ " "+word[0])
            
    with open("demo.json", "a", encoding="utf8") as file:
        json.dump(pos_tag, file)

for page in range(0, 60, 10): 
    try:
        url = generate_url('web developer', 'Canada', page)
        response = requests.get(url, headers)
        soup = BeautifulSoup(response.text , 'html.parser')
        card = soup.find_all('div', class_ = 'slider_container')
        no_jobs= len(card)
        for job in card:
            record(job)
    except:
        with open("count.txt", "w") as record:
            record.write(str(page))
        print("ended")