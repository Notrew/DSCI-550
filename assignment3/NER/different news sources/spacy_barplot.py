import json
import spacy
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

#load data from OCR
f = open('result.json')
data = json.load(f)

#get dates from json
dates = []
for i in data['aljazeera']:
    dates.append(i)
dates_update = dates[11:]

#get entity using spacy
nlp = spacy.load("en_core_web_sm")

comp_dict = {}
fox_json = {}
for i in dates_update:
    text = data['fox'][i]
    doc = nlp(text)
    person_d = []
    norp_d = []
    fac_d = []
    org_d = []
    gpe_d = []
    loc_d = []
    product_d = []
    event_d = []
    date_d = []
    time_d = []
    docdate_d = []
    dic = {}
    for entity in doc.ents:
        if entity.label_ == 'PERSON':
            person_d.append(entity.text)
        elif entity.label_ == 'NORP':
            norp_d.append(entity.text)
        elif entity.label_ == 'FAC':
            fac_d.append(entity.text)
        elif entity.label_ == 'ORG':
            org_d.append(entity.text)
        elif entity.label_ == 'GPE':
            gpe_d.append(entity.text)
        elif entity.label_ == 'LOC':
            loc_d.append(entity.text)
        elif entity.label_ == 'PRODUCT':
            product_d.append(entity.text)
        elif entity.label_ == 'EVENT':
            event_d.append(entity.text)
        elif entity.label_ == 'DATE':
            date_d.append(entity.text)
        elif entity.label_ == 'TIME':
            time_d.append(entity.text)
    dic['PERSON'] = person_d
    dic['NORP'] = norp_d
    dic['FAC'] = fac_d
    dic['ORG'] = org_d
    dic['GPE'] = gpe_d
    dic['LOC'] = loc_d
    dic['PRODUCT'] = product_d
    dic['EVENT'] = event_d
    dic['DATE'] = date_d
    dic['TIME'] = time_d
    fox_json[i] = dic

#aggragete info for barplots
person = []
norp = []
fac = []
org = []
gpe = []
loc = []
product = []
event = []
date = []
time = []
docdate = []
# Process whole documents
dic = {}
for i in dates_update:
    text = data['cnn'][i]
    doc = nlp(text)

    for entity in doc.ents:
        if entity.label_ == 'PERSON':
            person.append(entity.text)
        elif entity.label_ == 'NORP':
            norp.append(entity.text)
        elif entity.label_ == 'FAC':
            fac.append(entity.text)
        elif entity.label_ == 'ORG':
            org.append(entity.text)
        elif entity.label_ == 'GPE':
            gpe.append(entity.text)
        elif entity.label_ == 'LOC':
            loc.append(entity.text)
        elif entity.label_ == 'PRODUCT':
            product.append(entity.text)
        elif entity.label_ == 'EVENT':
            event.append(entity.text)
        elif entity.label_ == 'DATE':
            date.append(entity.text)
        elif entity.label_ == 'TIME':
            time.append(entity.text)

entity = [person,norp,org, gpe, loc]
entity_name = ['person','norp','org', 'gpe', 'loc']
bars = []

for i in range(len(entity)):
    my_df = pd.DataFrame({'mycolumn': entity[i]})
    p = my_df.mycolumn.value_counts()[:20].plot.bar(color = 'blue')
    p.set_title('CNN '+entity_name[i])
    p.figure
    bars.append(p.figure)