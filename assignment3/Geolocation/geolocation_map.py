#!/usr/bin/env python
# coding: utf-8

import os
import json
import spacy
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from functools import reduce
import PIL
import io
import geopandas as gpd

cnn_j = open('cnn.json')
fox_j = open('fox.json')
al_j = open('aljazeera.json')
# returns JSON object as
# a dictionary
cnn_json = json.load(cnn_j)
fox_json = json.load(fox_j)
al_json = json.load(al_j)

cnn_gpe = pd.DataFrame({'country':['China','Germany']})
fox_gpe = pd.DataFrame({'country':['China','Germany']})
al_gpe = pd.DataFrame({'country':['China','Germany']})

for date in cnn_json:
    tmp_df = pd.DataFrame({date: list(Counter(cnn_json[date]['GPE']).values()),'country': list(Counter(cnn_json[date]['GPE']).keys())})
    cnn_gpe = pd.merge(cnn_gpe,tmp_df,on = 'country',how = 'outer')
cnn_gpe = cnn_gpe.iloc[:,:20].fillna(0)
cnn_gpe.columns = ['country','03-12-22',
 '03-13-22',
 '03-14-22',
 '03-15-22',
 '03-16-22',
 '03-17-22',
 '03-18-22',
 '03-19-22',
 '03-20-22',
 '03-21-22',
 '03-22-22',
 '03-23-22',
 '03-24-22',
 '03-25-22',
 '03-26-22',
 '03-27-22',
 '03-28-22',
 '03-29-22',
 '03-30-22']    

for date in al_json:
    tmp_df = pd.DataFrame({date: list(Counter(al_json[date]['GPE']).values()),'country': list(Counter(al_json[date]['GPE']).keys())})
    al_gpe = pd.merge(al_gpe,tmp_df,on = 'country',how = 'outer')
al_gpe = al_gpe.iloc[:,:20].fillna(0)
al_gpe.columns = ['country','03-12-22',
 '03-13-22',
 '03-14-22',
 '03-15-22',
 '03-16-22',
 '03-17-22',
 '03-18-22',
 '03-19-22',
 '03-20-22',
 '03-21-22',
 '03-22-22',
 '03-23-22',
 '03-24-22',
 '03-25-22',
 '03-26-22',
 '03-27-22',
 '03-28-22',
 '03-29-22',
 '03-30-22']    

for date in fox_json:
    tmp_df = pd.DataFrame({date: list(Counter(fox_json[date]['GPE']).values()),'country': list(Counter(fox_json[date]['GPE']).keys())})
    fox_gpe = pd.merge(fox_gpe,tmp_df,on = 'country',how = 'outer')
fox_gpe = fox_gpe.iloc[:,:20].fillna(0)
fox_gpe.columns = ['country','03-12-22',
 '03-13-22',
 '03-14-22',
 '03-15-22',
 '03-16-22',
 '03-17-22',
 '03-18-22',
 '03-19-22',
 '03-20-22',
 '03-21-22',
 '03-22-22',
 '03-23-22',
 '03-24-22',
 '03-25-22',
 '03-26-22',
 '03-27-22',
 '03-28-22',
 '03-29-22',
 '03-30-22']    

al_gpe_index = al_gpe.set_index('country')
cnn_gpe_index = cnn_gpe.set_index('country')
fox_gpe_index = fox_gpe.set_index('country')
df_all = reduce(lambda a, b: a.add(b, fill_value=0), [cnn_gpe_index, al_gpe_index, fox_gpe_index])

world = gpd.read_file('./IPUMSI_world_release2020/world_countries_2020.shp')

world.replace('Viet Nam', 'Vietnam', inplace = True)
world.replace('Korea, Republic of', 'Korea', inplace = True)
world.replace('Iran (Islamic Republic of)', 'Iran', inplace = True)
world.replace('United States', 'US', inplace = True)
world.columns = ['OBJECTID','country','CNTRY_CODE','BPL_CODE','geometry']

merged_map = pd.merge(world,df_all,on = 'country',how = 'left').fillna(0)

image_frames = []
for dates in merged_map.columns.to_list()[5:24]:
    ax = merged_map.plot(column = dates, cmap = 'OrRd', figsize = (14,14),
                    legend = True, edgecolor = 'black', linewidth = 0.4)
    ax.set_title('Countries Mentioned in Daily News')
    ax.set_axis_off()
    img = ax.get_figure()
    
    f = io.BytesIO()
    img.savefig(f, format = 'png', bbox_inches = 'tight')
    f.seek(0)
    image_frames.append(PIL.Image.open(f))
    print(str(dates)+' done')

image_frames[0].save('countries_map.gif', format = 'GIF',
                    append_images = image_frames[1:],
                    save_all = True, duration = 300,
                    loop = 1)
#f.close()