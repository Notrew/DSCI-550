import pandas as pd
import json

with open('./Global_Landslide_Catalog_Export.json','r',encoding='utf8')as fp:
    json_data = json.load(fp)


#transfer it into dataframe format and select needed columns
rawlsd = pd.DataFrame(json_data).T
needed=["country_name","event_id","fatality_count","injury_count"]
lsd=rawlsd[needed]
lsd=lsd[lsd["country_name"].notnull()]


#calculate enents happened,fatality and injury number
cnt_id=lsd.groupby(["country_name"])[["event_id"]].count()
sum_fat=lsd.groupby(["country_name"])[["fatality_count"]].sum()
sum_inj=lsd.groupby(["country_name"])[["injury_count"]].sum()

lsd=cnt_id.merge(sum_fat,left_on="country_name",right_on="country_name").merge(sum_inj,left_on="country_name",right_on="country_name")


#standarize name
lsd=lsd.rename(index={"United States": "USA", "United Kingdom": "UK", "South Korea": "Korea"})


#read bik with publication rate
with open('./bik_Pub.csv','r',encoding="cp1254",errors="ignore")as fp:
    bik=pd.read_csv(fp)


#merge them and output bik with publication rate and landslide
merged=pd.merge(bik,lsd,left_on="Region",right_on="country_name")
merged.to_csv("./bik_Pub_landslide.csv")

