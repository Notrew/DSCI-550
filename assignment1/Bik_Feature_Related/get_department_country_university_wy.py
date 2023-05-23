
import requests
from lxml import etree
import time
import random
from html.parser import HTMLParser
import pandas as pd
import chardet
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.keys import Keys


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1"
}


#check encoding method
path = "./Bik dataset - papers with endpoint reached.tsv"     
f = open(path,'rb')
data = f.read()
encode=chardet.detect(data)["encoding"]
print(encode)


#read Bik dataset
with open('./Bik dataset - papers with endpoint reached.tsv','r',encoding="cp1254",errors="ignore")as fp:
    bik=pd.read_csv(fp,sep='\t')
#bik=bik[193:]


#select needed columns(title,citation,doi) and select my part
doi=bik[["Title","Citation","DOI"]]
doi=doi.iloc[193:214]


#create citation list
citation_lst=doi["Citation"].tolist()
citations=[]
for i in citation_lst:
    citations.append(i)


#create url list whose url can lead to article page directly
doi_lst=doi["DOI"].tolist()
for i in range(len(doi_lst)):
    doi_lst[i]=doi_lst[i].lstrip()
urls=[]
for i in doi_lst:
    url = "https://doi.org/" + i.replace(" ","")
    urls.append(url)


#to get html page
def get_html(url): 
    rep = requests.get(url, headers=headers)
    rep.encoding = 'utf-8'
    html = etree.HTML(rep.text)
    return html


#to simulate a chrome browser and get author affiliation of articles on cancer cell 
def clickCancerCell(url): 
    chrome_options = Options()
    chrome_options.add_argument('--headless') 
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)
    try:
        time.sleep(10)
        driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
    except:
        time.sleep(500)
        driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
    driver.find_element_by_xpath('.//li[@class="loa__item author"][1]').click()
    try:
        author_aff=driver.find_element_by_xpath('//*[@id="articleHeader"]/div/div[3]/div[2]/ul/li[1]//div[@class="article-header__info__group"][2]/div')
    except:
        author_aff=driver.find_element_by_xpath('//*[@id="articleHeader"]/div/div[3]/div[2]/ul/li[1]//div[@class="article-header__info__group"][1]/div')
    a=author_aff.text.split('\n')[0]
    driver.quit()
    return a


#to identify university of author affiliation of articles on oncology
def uni_ONCOLOGY(list):
    for i in list:
        if "University" in i:
            uni=i
            break
        if i==list[-1]:
            uni=list[1]
    return uni


#to identify university of author affiliation of articles on cancer cell
def uni_Cancer_Cell(list):
    for i in list:
        if "University" in i:
            uni=i
            break
        elif "School" in i:
            uni=i
            break
        else:
            uni=list[1]
    return uni


#to simulate a chrome browser and get author affiliation of articles on pubmed
def pubmed_search(d): 
    chrome_options = Options()
    chrome_options.add_argument('--headless') 
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://pubmed.ncbi.nlm.nih.gov/23302695/")
    try:
        time.sleep(10)
        className = driver.find_element_by_id('id_term')
        className.send_keys(d) 
        className.send_keys(Keys.ENTER)
    except:
        time.sleep(500)
        className = driver.find_element_by_id('id_term')
        className.send_keys(doi) 
        className.send_keys(Keys.ENTER)
    driver.find_element_by_xpath('//*[@id="toggle-authors"]/span').click()
    e=driver.find_element_by_xpath('//*[@id="full-view-expanded-authors"]/div/ul/li')
    e=e.text.split('\n')[1]
    driver.quit()
    return e


#to identify university of author affiliation of articles on pnas
def uni_pnas(list):
    for i in list:
        if "University" in i:
            uni=i
            break
        elif "School" in i:
            uni=i
            break
        elif "Institute" in i:
            uni=i
            break
    return uni


#create lisr of author affiliation and complete it
author_affs=[]

for i in range(len(urls)):
    url=urls[i]
    #print(url)
    html=get_html(url)
    if i<=0:
        author_aff=html.xpath('//*[@id="authorInfoFullList"]/div[1]/div[2]/div[2]/div/text()')[0]
        author_affs.append(author_aff)
    elif i>0 and i<=9:
        author_aff=html.xpath('/html/head/meta[8]/@content')[0]
        author_affs.append(author_aff)
    elif i>9 and i<=14:
        author_aff=clickCancerCell(url)
        #print(author_aff)
        author_affs.append(author_aff)
    else:
        author_aff=pubmed_search(doi_lst[i])
        author_affs.append(author_aff)


#create lists of department, university and region, and complete them
departments=[]
universities=[]
regions=[]
for i in range(len(author_affs)): 
    strs=author_affs[i].split(",")
    if i<=0:
        departments.append(strs[1].lstrip())
        universities.append(strs[0])
        region=strs[-1].lstrip()
        regions.append(region)
    elif i>0 and i<=9:
        dep=strs[0].lstrip()
        departments.append(dep)
        uni=uni_ONCOLOGY(strs).lstrip()
        universities.append(uni)
        region=strs[-1].lstrip()
        #standarize region name
        if region=='P.R. China':
            region="China"
        elif region=="Republic of Korea":
            region="Korea"
        elif region=="R.O.C.":
            region="Taiwan"
        regions.append(region)
    elif i>9 and i<=14:
        dep=strs[0].lstrip()
        departments.append(dep)
        uni=uni_Cancer_Cell(strs).lstrip()
        universities.append(uni)
        region=strs[-1].lstrip()
        regions.append(region)
    else:
        dep=strs[0].lstrip()
        departments.append(dep)
        uni=uni_pnas(strs).lstrip()
        universities.append(uni)
        region=strs[-1].lstrip()
        if region=="Canada K7L 3N6.":
            region="Canada"
        if region=="United Kingdom.":
            region="UK"
        region=region.replace(".","")
        regions.append(region)


#combine three lists to a dictionary and change its index in order to merge with my part of bik better
dict={"department":departments,"university":universities,"region":regions}
df=pd.DataFrame(dict)
df=df.rename(lambda x: x+193, axis=0)


#merge department, university and region with bik
df1=pd.concat([bik[193:214],df],axis=1)
df1=df1[:214]


#output merged dataset in csv format
df1.to_csv("193-213.csv")

