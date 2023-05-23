import pandas as pd
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup

# Import the Bik dataset
bik = pd.read_csv('Bik.tsv', sep='\t')


# Modify some DOIs for concatenation to a universal url
# NOTE: Manually searched for these DOIs based on the paper title
bik.at[51, 'DOI'] = '10.1128/IAI.64.6.2282-2287.1996'
bik.at[52, 'DOI'] = '10.1128/IAI.67.1.80-87.1999'
bik.at[80, 'DOI'] = '10.1128/JCM.36.6.1666-1673.1998'


# I was in charge of the first 91 papers published in PLOS, mBio, Infectoin and Immunity, and J. Clinical Microbio
data = bik.iloc[0: 91, :]


# Generate a list of DOIs
DOIs = data['DOI'].tolist()


# Generate a list of urls by concatenating DOIs to corresponding urls
urls = []
for i in range(len(DOIs)):
    # PLOS
    if i < 48:
        url = 'https://journals.plos.org/plosntds/article/authors?id=' + str(DOIs[i])
        urls.append(url)
    # mBio, Infection and Immunity, and J. Clinical Microbio
    else:
        url = 'https://journals.asm.org/doi/' + DOIs[i]
        urls.append(url)


# Use selenium webdriver to extract content from dynamic websites
# NOTE: May need to change the chromedriver path based on where the chromedriver is stored at
def render(url):
    driver = webdriver.Chrome(executable_path = './chromedriver')
    driver.get(url)
    time.sleep(3)
    r = driver.page_source
    driver.quit()
    return r


# Generate a list of affiliations
affiliations = []
for i in range(len(urls)):
    # PLOS
    if i < 48:
        page = requests.get(urls[i])
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.find('p', attrs = {'id': 'authAffiliations-0'}).get_text()
        # Some modifications to each affiliation
        text = text.replace('Affiliation\n    ', '').replace('Affiliations\n    ', '').replace('\n    ', '').strip().split(', ')
        affiliations.append(text)
    # mBio, Infectoin and Immunity, and J. Clinical Microbio
    else:
        page = render(urls[i])
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.find('div', attrs = {'class': 'affiliations'}).get_text()
        # Some modifications to each affiliation
        text = text.strip().split(', ')
        affiliations.append(text)


# Keys for some matching and replacing
key1 = ['Australia', 'Brazil', 'Chile', 'China', 'France', 'Germany', 'Hong Kong', 'India', 'Israel', 'Italy', 'Japan', 
       'Korea', 'Malaysia', 'Poland', 'Singapore', 'Slovenia', 'Spain', 'Sweden', 'United Kingdom', 
        'United States of America']
key2 = ['USA', 'USA.', 'United States', 'Colorado', 'Massachusetts', 'Minnesota', 'Nebraska', 'North Carolina', 'Ohio',
        'Oregon']
key3 = ['University', 'College', 'Academy', 'Institute', 'Tech']


# Extract countries
country = []
for i in range(len(affiliations)):
    ctry = ''
    for k1 in range(len(key1)):
        # Region is usually the last string in one affiliation list
        a = affiliations[i][-1]
        if key1[k1] in a:
            ctry = a
    for k2 in range(len(key2)):
        # Sometimes the last string is a US state/abbreviation, so replace it
        b = affiliations[i][-1]
        if key2[k2] in b:
            ctry = 'United States of America'
    country.append(ctry)


# Extract universities
university = []
for i in range(len(affiliations)):
    univ = ''
    for str in range(len(affiliations[i])):
        string = affiliations[i][str]
        for k in range(len(key3)):
            # Use keywords in key3 to look for the university element
            if key3[k] in string:
                univ = string
    university.append(univ)


# Extract degree area
area = []
for i in range(len(affiliations)):
    # We set the rule that the degree area is based on the author's affiliated department
    a = affiliations[i][0]
    # Remove common phrases to obtain the degree area only
    # NOTE: there were some manual modifications in the exported data because there're too many special cases
    a = a.replace('Institute of ', '').replace('Department of ', '').replace('Discipline of ', '')
    a = a.replace('School of ', '').replace('University of Glasgow ', '').replace('Departments of ', '')
    a = a.replace('National Creative Research Initiatives Center for ', ''). replace('Department ', '')
    a = a.replace('Division of ', '').replace('State Key Laboratory for ', '').replace('Key Laboratory of ', '')
    a = a.replace('the Centre for ', '').replace('Advanced Laboratory for ', '').replace('Program in ', '')
    a = a.replace('Center for ', '').replace('Program on ', '').replace('Laboratory of ', '')
    area.append(a)


# We set the rule on some country names: USA, UK, Korea, China
for i in range(len(country)):
    if country[i] == 'United States of America':
        country[i] = 'USA'
    elif country[i] == 'United Kingdom':
        country[i] = 'UK'
    elif country[i] == 'Republic of Korea':
        country[i] = 'Korea'
    elif country[i] == 'P. R. China':
        country[i] = 'China'
    elif country[i] == "People's Republic of China":
        country[i] = 'China'


# Combine the features for export
df = pd.DataFrame()
df['country'] = country
df['university'] = university
df['area'] = area


# Export a csv file containing the features
# NOTE: the features were copied and pasted to the Bik data
compression_opts = dict(method='zip', archive_name='Ziyue_paper_features.csv')  
df.to_csv('Ziyue_paper_features.zip', index=False, compression = compression_opts)  



