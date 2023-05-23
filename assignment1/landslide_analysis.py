#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from math import*
from scipy.spatial import distance
from scipy.spatial.distance import cityblock
from scipy import spatial
from sklearn.metrics import jaccard_score
from sklearn.cluster import KMeans
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from matplotlib.font_manager import FontProperties
from matplotlib.colors import ListedColormap
from scipy.misc import imread
from imageio import imread

plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.unicode_minus']=False



bik_df = pd.read_csv('bik_Pub.csv')
landslide = pd.read_csv('Landslide_data.csv')


#clean the landslide data
landslide['Fatality Count'] = landslide['Fatality Count'].str.replace(",","").astype(float)
landslide['Event Id'] = landslide['Event Id'].fillna(0)
landslide['Fatality Count'] = landslide['Fatality Count'].fillna(0)
landslide['Injury Count'] = landslide['Injury Count'].fillna(0)


#aggregate landslide data by region
d = {'event_cnt':landslide.groupby('_Country Name')['Event Id'].sum(),
    'fatality_cnt':landslide.groupby('_Country Name')['Fatality Count'].sum(),
    'injury_cnt':landslide.groupby('_Country Name')['Injury Count'].sum()}
landslide_df = pd.DataFrame(data=d)


#merge the landslide data with original bik data
landslide_df = landslide_df.rename(index={'United States': 'USA', 'United Kingdom':'UK', 'South Korea':'Korea'})
landslide_df['Region'] = landslide_df.index 


new_df = bik_df.merge(landslide_df, on='Region', how='left')



#count publications in each region
d1 = {'publication_cnt':new_df.groupby(['Region'])['Title'].nunique()}
df1= pd.DataFrame(data=d1)



#merge aggregated landslide data with region publication data
agg_landslide = df1.merge(landslide_df, on='Region', how='left')
agg_landslide = agg_landslide.fillna(0)



#visualize the data
fig,ax = plt.subplots(figsize=(16,9), dpi = 100)
width = 0.8
pos = [*range(31)]
col2 = "lightseagreen"
col1 = "darkorange"

ax.bar(pos, agg_landslide.publication_cnt, color = 'grey', alpha=.7,label = "Publications", linewidth = 3, width = 0.5, edgecolor = "white")
for i,v in enumerate(agg_landslide.publication_cnt):
    ax.text(i, agg_landslide.publication_cnt[i]+0.2, int(agg_landslide.publication_cnt[i]**2), fontweight="bold", 
            fontname='Arial', fontsize = 16, ha='center', va = "center")

ax2 = ax.twinx()
ax2.plot(pos, agg_landslide.event_cnt, marker = "o", markeredgecolor = "white", color = "orange",
         markersize=20,linestyle='--',linewidth=0.1,alpha=.8,
         markeredgewidth = 2, label = 'Landslide Count')

ax2.plot(pos, agg_landslide.fatality_cnt, marker = "o", markeredgecolor = "white", 
         color = "red", markersize=20,linestyle='--',linewidth=0.1,alpha=.4,
         markeredgewidth = 2, label = 'Fatality Count')


ax.set_ylim(0,8.7)
ax2.set_ylim(0,1100)
plt.xticks(pos, agg_landslide.Region, rotation = 45)
ax.set_title("Publications and Landslides by Countries", loc = "center", fontdict = {"fontsize":24,"fontweight":"bold"})
ax.xaxis.set_tick_params(labelsize=14, rotation = 90)
ax2.set_yticklabels([])
ax.set_yticklabels([])

bar1, labels1 = ax.get_legend_handles_labels()
bar2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(
    bar1 + bar2[:3], labels1 + labels2[:3],
    loc="upper center", fontsize='large',shadow=True, 
    frameon=True, facecolor = "white", ncol = 4)

ax2.grid(False)

fig.tight_layout()
plt.show()



ana_data = df1.merge(landslide_df, on='Region', how='left')
ana_data = ana_data.fillna(0)



#calculate correlations of publications and landslides
corr_mat = ana_data.corr()
sns.heatmap(corr_mat, annot=True, cmap = 'YlGnBu')
plt.title('Correlation Matrix', fontsize = 20) # title with fontsize 20
plt.xlabel('',fontsize = 12) # x-axis label with fontsize 15
plt.ylabel('',fontsize = 12)
plt.show()




#calculate manhattan distance
manhattan_res = {'to_event':cityblock(ana_data['publication_cnt'],ana_data['event_cnt']),
                 'to_fatality':cityblock(ana_data['publication_cnt'],ana_data['fatality_cnt']),
                 'to_injury':cityblock(ana_data['publication_cnt'],ana_data['injury_cnt'])}
print(manhattan_res)



#calculate euclidean distance
euclidean_res = {'to_event':distance.euclidean(ana_data['publication_cnt'],ana_data['event_cnt']),
                 'to_fatality':distance.euclidean(ana_data['publication_cnt'],ana_data['fatality_cnt']),
                 'to_injury':distance.euclidean(ana_data['publication_cnt'],ana_data['injury_cnt'])}
print(euclidean_res)



#calculate cosine similarity
cosine_similarity = {'to_event':1 - spatial.distance.cosine(ana_data['publication_cnt'],ana_data['event_cnt']),
                 'to_fatality':1 - spatial.distance.cosine(ana_data['publication_cnt'],ana_data['fatality_cnt']),
                 'to_injury':1 - spatial.distance.cosine(ana_data['publication_cnt'],ana_data['injury_cnt'])}
print(cosine_similarity)



#analyze relationship between lab size and landslide occurrance
bik_full = pd.read_csv('bik_pub_landslide_ranking_labsize_country.csv')
bik_full = bik_full.fillna(0)
cluster_df = bik_full[['Lab Size','event_cnt']].to_numpy()

#K-means clustering
kmeans = KMeans(n_clusters= 5)
label = kmeans.fit_predict(cluster_df)
 
u_labels = np.unique(label)


for i in u_labels:
    plt.scatter(cluster_df[label == i , 0] , cluster_df[label == i , 1] , label = i)
plt.xlabel('Lab Size', fontsize=16)
plt.ylabel('Landslide', fontsize=16)
plt.legend()
plt.show()

