#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd


# In[ ]:


cos_all_fearures=pd.read_csv('./cos_bik_all_features.csv')
cos_bik_aff_labsize_otherpub_pub_landslide_ranking=pd.read_csv('./cos_bik_aff_labsize_otherpub_pub_landslide_ranking.csv')
cos_bik_aff_labsize_otherpub_pub_landslide=pd.read_csv('./cos_bik_aff_labsize_otherpub_pub_landslide.csv')
cos_bik_aff_labsize_otherpub_pub=pd.read_csv('./cos_bik_aff_labsize_otherpub_pub.csv')
cos_bik_aff_labsize_otherpub=pd.read_csv('./cos_bik_aff_labsize_otherpub.csv')
cos_bik_aff_labsize=pd.read_csv('./cos_bik_aff_labsize.csv')
cos_bik_aff=pd.read_csv('./cos_bik_aff.csv')
cos_bik=pd.read_csv('./cos_bik.csv')


# In[ ]:


all_fearures=cos_all_fearures.describe()["Similarity_score"]
bik_aff_labsize_otherpub_pub_landslide_ranking=cos_bik_aff_labsize_otherpub_pub_landslide_rankinge.describe()["Similarity_score"]
bik_aff_labsize_otherpub_pub_landslide=cos_bik_aff_labsize_otherpub_pub_landslide.describe()["Similarity_score"]
bik_aff_labsize_otherpub_pub=cos_bik_aff_labsize_otherpub_pub.describe()["Similarity_score"]
bik_aff_labsize_otherpub=cos_bik_aff_labsize_otherpub.describe()["Similarity_score"]
bik_aff_labsize=cos_bik_aff_labsize.describe()["Similarity_score"]
bik_aff=cos_bik_aff.describe()["Similarity_score"]
bik=cos_bik.describe()["Similarity_score"]


# In[ ]:


a = pd.concat([bik,bik_aff,bik_aff_labsize,bik_aff_labsize_otherpub,bik_aff_labsize_otherpub_pub], axis=1)
a=a[1:]
a.columns=['bik','bik_aff','bik_aff_labsize','bik_aff_labsize_otherpub','bik_aff_labsize_otherpub_pub']
print(a)


# In[ ]:


b = pd.concat([bik_aff_labsize_otherpub_pub,bik_aff_labsize_otherpub_pub_landslide,bik_aff_labsize_otherpub_pub_landslide_ranking,all_fearures], axis=1)
b=b[1:]
b.columns=['bik_aff_labsize_otherpub_pub','bik_aff_labsize_otherpub_pub_landslide','bik_aff_labsize_otherpub_pub_landslide_ranking','all_features']
print(b)

