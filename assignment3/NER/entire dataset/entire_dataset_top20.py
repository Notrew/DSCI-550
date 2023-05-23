#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# aljazeera entities
f = open('aljazeera.json')
aljazeera = json.load(f)
al_person = aljazeera['PERSON']
al_norp = aljazeera['NORP']
al_org = aljazeera['ORG']
al_gpe = aljazeera['GPE']
al_loc = aljazeera['LOC']

# cnn entities
f = open('cnn.json')
cnn = json.load(f)
cnn_person = cnn['PERSON']
cnn_norp = cnn['NORP']
cnn_org = cnn['ORG']
cnn_gpe = cnn['GPE']
cnn_loc = cnn['LOC']

# fox entities
f = open('fox.json')
fox = json.load(f)
fox_person = fox['PERSON']
fox_norp = fox['NORP']
fox_org = fox['ORG']
fox_gpe = fox['GPE']
fox_loc = fox['LOC']



# PERSON top20 dataframe
person = al_person + cnn_person + fox_person
person_df = pd.DataFrame()
person_df['PERSON'] = person

person_count = person_df['PERSON'].value_counts().reset_index()
person_count.columns = ['PERSON', 'Count']
person_top20 = person_count.iloc[0:20]
person_top20

# PERSON top20 barplot
ax = sns.barplot(x = 'PERSON', y = 'Count', data = person_top20, color = 'red')
ax.set_title('Entire Dataset: Top 20 Mentioned PERSON', fontsize = 15)
ax.bar_label(ax.containers[0])

sns.set(rc = {'figure.figsize':(10,5)})
plt.xticks(rotation = 90, horizontalalignment = "center")
plt.show()



# NORP top20 dataframe
norp = al_norp + cnn_norp + fox_norp
norp_df = pd.DataFrame()
norp_df['NORP'] = norp

norp_count = norp_df['NORP'].value_counts().reset_index()
norp_count.columns = ['NORP', 'Count']
norp_top20 = norp_count.iloc[0:20]
norp_top20

# NORP top20 barplot
ax = sns.barplot(x = 'NORP', y = 'Count', data = norp_top20, color = 'orange')
ax.set_title('Entire Dataset: Top 20 Mentioned NORP', fontsize = 15)
ax.bar_label(ax.containers[0])

sns.set(rc = {'figure.figsize':(10,5)})
plt.xticks(rotation = 90, horizontalalignment = "center")
plt.show()



# ORG top20 dataframe
org = al_org + cnn_org + fox_org
org_df = pd.DataFrame()
org_df['ORG'] = org

org_count = org_df['ORG'].value_counts().reset_index()
org_count.columns = ['ORG', 'Count']
org_top20 = org_count.iloc[0:20]
org_top20

# ORG top20 barplot
ax = sns.barplot(x = 'ORG', y = 'Count', data = org_top20, color = 'yellow')
ax.set_title('Entire Dataset: Top 20 Mentioned ORG', fontsize = 15)
ax.bar_label(ax.containers[0])

sns.set(rc = {'figure.figsize':(10,5)})
plt.xticks(rotation = 90, horizontalalignment = "center")
plt.show()



# GPE top20 dataframe
gpe = al_gpe + cnn_gpe + fox_gpe
gpe_df = pd.DataFrame()
gpe_df['GPE'] = gpe

gpe_count = gpe_df['GPE'].value_counts().reset_index()
gpe_count.columns = ['GPE', 'Count']
gpe_top20 = gpe_count.iloc[0:20]
gpe_top20

# GPE top20 barplot
ax = sns.barplot(x = 'GPE', y = 'Count', data = gpe_top20, color = 'green')
ax.set_title('Entire Dataset: Top 20 Mentioned GPE', fontsize = 15)
ax.bar_label(ax.containers[0])

sns.set(rc = {'figure.figsize':(10,5)})
plt.xticks(rotation = 90, horizontalalignment = "center")
plt.show()



# LOC top20 dataframe
loc = al_loc + cnn_loc + fox_loc
loc_df = pd.DataFrame()
loc_df['LOC'] = loc

loc_count = loc_df['LOC'].value_counts().reset_index()
loc_count.columns = ['LOC', 'Count']
loc_top20 = loc_count.iloc[0:20]
loc_top20

# LOC top20 barplot
ax = sns.barplot(x = 'LOC', y = 'Count', data = loc_top20, color = 'blue')
ax.set_title('Entire Dataset: Top 20 Mentioned LOC', fontsize = 15)
ax.bar_label(ax.containers[0])

sns.set(rc = {'figure.figsize':(10,5)})
plt.xticks(rotation = 90, horizontalalignment = "center")
plt.show()


