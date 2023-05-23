#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


#Read the CSV file
df = pd.read_csv("countries_of_the_world_raw.csv")


# In[3]:


#See the first 5 data
df.head()


# In[4]:


df.info()


# In[5]:


#Change the datatypes of the three features below for further handling
df["Population"]=df["Population"].astype('str')
df["Area (sq. mi.)"]=df["Area (sq. mi.)"].astype('str')
df["GDP ($ per capita)"]=df["GDP ($ per capita)"].astype('str')


# In[6]:


#See the df in notebook
df


# In[7]:


#Change the ',' into '.' between integer and decimal digits
df['Pop. Density (per sq. mi.)'] = df['Pop. Density (per sq. mi.)'].astype(str).str.replace(',', '.').astype(float)
df['Coastline (coast/area ratio)'] = df['Coastline (coast/area ratio)'].astype(str).str.replace(',', '.').astype(float)
df['Net migration'] = df['Net migration'].astype(str).str.replace(',', '.').astype(float)
df['Infant mortality (per 1000 births)'] = df['Infant mortality (per 1000 births)'].astype(str).str.replace(',', '.').astype(float)
df['Literacy (%)'] = df['Literacy (%)'].astype(str).str.replace(',', '.').astype(float)
df['Phones (per 1000)'] = df['Phones (per 1000)'].astype(str).str.replace(',', '.').astype(float)
df['Arable (%)'] = df['Arable (%)'].astype(str).str.replace(',', '.').astype(float)
df['Crops (%)'] = df['Crops (%)'].astype(str).str.replace(',', '.').astype(float)
df['Other (%)'] = df['Other (%)'].astype(str).str.replace(',', '.').astype(float)
df['Birthrate'] = df['Birthrate'].astype(str).str.replace(',', '.').astype(float)
df['Deathrate'] = df['Deathrate'].astype(str).str.replace(',', '.').astype(float)
df['Agriculture'] = df['Agriculture'].astype(str).str.replace(',', '.').astype(float)
df['Industry'] = df['Industry'].astype(str).str.replace(',', '.').astype(float)
df['Service'] = df['Service'].astype(str).str.replace(',', '.').astype(float)


# In[8]:


#Change the country name to match with the other datasets
df.loc[110,"Country"]="Korea"
df.loc[213,"Country"]="UK"
df.loc[214,"Country"]="USA"


# In[9]:


#Delete all the additional space that comes after country name
df["Country"]=df["Country"].str.rstrip()


# In[10]:


#Create a new dataframe containing the below three features
df_country = df.loc[:,["Country","GDP ($ per capita)","Literacy (%)","Pop. Density (per sq. mi.)"]]


# In[11]:


#Change the name of "Country" feature into "Region"
df_country = df_country.rename(columns={'Country':'Region'})


# In[12]:


#Output the updated country csv file
df_country.to_csv("countries of the world.csv")


# In[13]:


#Load the Bik dataset
df_BIK = pd.read_csv("bik_pub_landslide_ranking_labsize.csv",encoding = 'unicode_escape')


# In[14]:


#Check the datatype of each column in the dataset
df_BIK.info()


# In[15]:


#See the df_BIK in notebook
df_BIK


# In[16]:


#Merge the country dataset with the Bik dataset by using left join and set key as "Region"
merged_df = pd.merge(df_BIK, df_country, how="left", on=["Region"])


# In[17]:


#See the merged_df in notebook
merged_df


# In[18]:


#Output the final merged csv file
merged_df.to_csv("bik_pub_landslide_ranking_labsize_country.csv")


# In[19]:


#Create a new dataframe containing the count of each country's total occurrences
df1 = merged_df.groupby('Region').size().reset_index(name="country_count")


# In[20]:


#See the df1 dataframe in Notebook
df1


# In[21]:


#Merge df1 with df_country by left join and set key as "Region" in order to further analyze correlation
df2= pd.merge(df1, df_country, how="left", on=["Region"])


# In[22]:


#See the df2 dataframe in Notebook
df2


# In[23]:


#See the information of each columns in the df2 dataframe
df2.info()


# In[24]:


#Change the GDP's datatype to float
df2["GDP ($ per capita)"]=df2["GDP ($ per capita)"].astype('float')


# In[25]:


#Get the correlation in df2
corr=df2.corr()
corr


# In[26]:


#Draw a heatmap based on the correlation of df2
import seaborn as sns
sns.heatmap(corr,cmap='Blues',annot=True,square=True,fmt='.3f')


# In[ ]:




