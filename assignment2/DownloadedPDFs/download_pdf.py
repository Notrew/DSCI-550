#!/usr/bin/env python
# coding: utf-8

# In[2]:



from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import os


data = pd.read_csv('PMC.csv',names = 'P')


l_pmc = list(data['P'])
l_pmc[0]


driver = webdriver.Chrome(executable_path=r"/Users/teresashang/Downloads/chromedriver")

for i in l_pmc:
    driver.get("https://www.ncbi.nlm.nih.gov/pmc/articles/"+i+"/pdf/")


data = pd.read_csv('pdfs.csv')
pdfs = data['pdfs'].to_list()

