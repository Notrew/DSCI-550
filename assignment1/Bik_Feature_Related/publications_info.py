#!/usr/bin/env python
# coding: utf-8



#get first author publications, career years and publication rate

from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import pandas as pd
import numpy as np
from math import*




#get first author names
data = pd.read_csv('bik.csv')
authors = list(data['First Author'])




#download files which contains author's publications information

for i in authors[126:]:
    driver.get("https://pubmed.ncbi.nlm.nih.gov/?term="+i)
    driver.find_element_by_css_selector("button#side-download-results-by-year-button.download-results-by-year-button").click()




with open('all.txt') as f:
    lines = f.readlines()

#process all downloaded files
i = 0
data = []
for i in range(len(lines)):
    if 'Search query' in lines[i]:
        name = lines[i].split(': ')[1].strip()
    elif 'Year' in lines[i]:
        name = name
    else: 
        info = name+','+lines[i].strip()
        data.append(info.split(','))
    


#data cleaning
df = pd.DataFrame (data, columns = ['name', 'year', 'count'])
df['year'] = pd.to_numeric(df['year'])
df['count'] = pd.to_numeric(df['count'])



#count each author's publications
df_res = pd.DataFrame(df.groupby('name')['count'].sum())
#get the career years by subtracting the most recent publication date with the earliest publication date
df_years = pd.DataFrame(df.groupby('name')['year'].agg(np.ptp))
df_res['years'] = df_years['year']
df_res['avg'] = round(df_res['count']/df_res['years'],2)
df_res['First Author'] = df_res.index
df_res = df_res.reset_index(drop=True)


data_author_info = pd.read_csv('bik.csv')



#merge information with the original dataset
res = data_author_info.set_index('First Author').join(df_res.set_index('First Author'))



res.to_csv('bik_Pub.csv')

