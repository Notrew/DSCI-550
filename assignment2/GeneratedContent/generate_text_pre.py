#!/usr/bin/env python
# coding: utf-8

# In[2]:




import pandas as pd
from datetime import datetime
import random
import time
import json

data = pd.read_csv('pdfs.csv')
pdfs = data['pdfs'].to_list()
#download fakenmes from Fake Name Generator
names = pd.read_csv('FakeName.csv')
names['Name'] = names['Surname']+' '+names['GivenName']

names2 = pd.read_csv('FakeName2.csv')
names2['Name'] = names2['Surname']+' '+names2['GivenName']

names3 = names2.iloc[100:]
names3 = names3.reset_index()

#generate random dates
a1=(1990,1,1,0,0,0,0,0,0)            
a2=(2010,3,26,23,59,59,0,0,0)   
start=time.mktime(a1)   
end=time.mktime(a2)     
posting_date=[]
for i in range(200):     
   t=random.randint(start,end)    
   date_touple=time.localtime(t)         
   date=time.strftime("%Y-%m-%d",date_touple)
   #time.strftime("%Y-%m-%d %H:%M:%S",date_touple)
   posting_date.append(date)

publish_date = []
for i in posting_date:
    publish_date.append(datetime.strptime(i, "%Y-%m-%d").strftime("%m-%d-%Y"))

#compile author names, titles, text, domain, summary and publish data to json file
multikeys = []
for i in range(len(pdfs)):
    dic = {}
    j_file = pdfs[i].replace('.pdf', '.json')
    f = open('pdf_content/'+j_file)
    content = json.load(f)
    #j = random. randint(0,190)
    dic['title'] = content[2500:2560]
    #dic['title'] = pdfs[i].replace('.pdf', '')
    dic['text'] = content
    dic['domain'] = names3['Domain'][i]
    dic['summary'] = content[800:1500]
    dic['authors'] = names3['Name'][i]
    dic['publish_date'] = publish_date[i]
    multikeys.append(dic)


with open('new_input.jsonl', 'w') as outfile:
    for entry in multikeys:
        json.dump(entry, outfile)
        outfile.write('\n')


