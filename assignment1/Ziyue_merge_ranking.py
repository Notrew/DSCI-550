import pandas as pd


# Import the dataset, which had piblication rate and landslide features merged by Wenting
bik = pd.read_csv('bik_pub_landslide.csv', index_col=[0])
bik = pd.DataFrame(bik)
bik


# Clean the university column for matching
bik['University'] = bik['University'].str.replace(' School of Medicine', '')
bik['University'] = bik['University'].str.replace(' Medical School', '')
bik['University'] = bik['University'].str.replace('Medical School of ', '')
bik['University'] = bik['University'].str.replace(' School of Dentistry', '')
bik['University'] = bik['University'].str.replace('Jiaotong', 'Jiao Tong')

bik['University'] = bik['University'].replace('Harvard', 'Harvard University')
bik['University'] = bik['University'].replace('Yale', 'Yale University')
bik['University'] = bik['University'].replace('Washington University', 'Washington University in St Louis')
bik['University'] = bik['University'].replace('The University of Hong Kong', 'University of Hong Kong')
bik['University'] = bik['University'].replace('The Ohio State University', 'Ohio State University')
bik['University'] = bik['University'].replace('The Johns Hopkins University', 'Johns Hopkins University')
bik['University'] = bik['University'].replace('Johns Hopkins University School', 'Johns Hopkins University')
bik['University'] = bik['University'].replace('University of Vermont College of Medicine', 'University of Vermont')
bik['University'] = bik['University'].replace('Korea University College of Medicine', 'Korea University')


# Import the world university ranking dataset and choose 2013 data
data = pd.read_csv('RawRanking.csv')
data = pd.DataFrame(data)
data = data[data['year'] == 2013].reset_index(drop=True)


# Extract selected features to a new dataframe
ranking = pd.DataFrame()
ranking['University'] = data['university_name']
ranking['World Rank'] = data['world_rank']
ranking['Teaching'] = data['teaching']
ranking['Research'] = data['research']


# Merge the two datasets on University
merge = pd.merge(bik, ranking, on='University', how='left')


# Export the merged dataset and pass it to Ziquan for merging the lab size
compression_opts = dict(method='zip', archive_name='bik_pub_landslide_ranking.csv')  
merge.to_csv('bik_pub_landslide_ranking.zip', index=False, compression = compression_opts)



