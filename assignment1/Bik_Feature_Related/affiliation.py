#! /usr/bin/python3
# -*- encoding: utf-8 -*-

from time import sleep
import requests as rqs
import pandas as pd
from lxml import etree
from selenium import webdriver as wb
import json

# different journal sources
part = ["Cytokine", "Science", "Nature", "Oncogene"]

# request_header
params = {
    "cookie": "EUID=655092bd-ff97-4739-b0ac-d10b620207a8; id_ab=AEG; mboxes={}; utt=a632-3ba88241f71426b6616-1a21148771b14b2a-0ta; has_multiple_organizations=false; sd_session_id=540722fd7a659643ea09c0932bef47b487e3gxrqa; ANONRA_COOKIE=E4831D57BF5CF8F3FA9D202A890215E82F650CC78E82CDA3008842E5DD17FEBEE2EC59925EF5E61DE63A3F252D2B6606950A616CA8667483; acw=540722fd7a659643ea09c0932bef47b487e3gxrqa|$|29B2D1E29972E49373400615522CB8922FA292256A97D6D84B78C7037CB54938F3811CCC059152845405528916BFD86B78DB225E54AABC8F3FBA44D1BD4E4F2EAFE9C31A29ED2080B6DA1F7CB1786ABB; fingerPrintToken=bccc69485298a057838da13fb48286c2; AMCVS_4D6368F454EC41940A4C98A6@AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6@AdobeOrg=-2121179033|MCIDTS|19043|MCMID|55374883806600201180582147712655249555|MCAAMLH-1645998985|9|MCAAMB-1645998985|RKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y|MCOPTOUT-1645401385s|NONE|MCAID|NONE|MCCIDH|1025084382|vVersion|5.3.0; MIAMISESSION=184930b4-793a-45d2-9f17-21ee15df48ef:3822850543; SD_REMOTEACCESS=eyJhY2NvdW50SWQiOiI1MTkwMSIsInRpbWVzdGFtcCI6MTY0NTM5Nzc0MzQ2Mn0=; mbox=session#63ce92dba8b743e585719bf05a4f105f#1645399604|PC#1aea64db50004dc687ced00b2b8371a5.34_0#1708642544; __cf_bm=3F4Prj.GL0akm4N5D0yO6khjctOrHsCqbuiNPdjcsIU-1645397743-0-Ae1b/kQoScEzYFex5BoK++lbeplHd8cEnQU+3W2Ip0vfXkTlqQbDhtgWkMQWF1IFro+z0KN5aeWgeDeLUF6BqkorFdMYWROF2YfYlKx9Skyf; s_pers= c19=sd%3Aproduct%3Ajournal%3Aarticle|1645399545610; v68=1645397743539|1645399545613; v8=1645397745619|1740005745619; v8_s=Less%20than%201%20day|1645399545619;; s_sess= s_cpc=0; s_ppvl=sd%253Aproduct%253Ajournal%253Aarticle%2C48%2C48%2C864%2C1159%2C864%2C1536%2C864%2C1.25%2CP; e41=1; s_cc=true; s_ppv=sd%253Aproduct%253Ajournal%253Aarticle%2C48%2C3%2C864%2C1144%2C742%2C1536%2C864%2C1.25%2CP;",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98";',
    "sec-ch-ua-platform": "Windows",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
}

# author affiliation result
author_ref = {}

# websriver
driver = wb.Chrome("./chromedriver.exe")


def decode(htmlstr: str) -> str:
    """Decode trasformed html text. 
    Coverting %Hex char into %unicode char.  

    Args:
        htmlstr (str): text contains %Hex char

    Returns:
        str: unicode string
    """
    while "%" in htmlstr:
        value = htmlstr.find("%")
        char = chr(int(htmlstr[value + 1 : value + 3], 16))
        htmlstr = htmlstr[:value] + char + htmlstr[value + 3 :]
    return htmlstr


def get_redirection_url(citation, primary_url: str) -> str:
    """Get Redirection website url.

    Args:
        citation (_type_): citation_source
        primary_url (str): https://doi.org/+DOI

    Returns:
        str: Redirected_url
    """
    res = rqs.get(primary_url, headers=params)
    html = etree.HTML(res.text)
    if part[0] in citation:
        raw_url = html.xpath('//input[@name = "redirectURL"]/@value')[0]
    elif part[1] in citation:
        raw_url = html.xpath("//meta[@property='og:url']/@content")[0]
    else:
        raw_url = primary_url
    redirect_url = decode(raw_url)
    return redirect_url


def get_author_affiliation(citation: str, url: str, driver) -> None:
    """
    This function aims to get authors affiliation.

    Args:
        citation (str): citation source
        url (str): website_url
        driver (_type_): Chrome_driver.
        
    """
    author_ref_local = {}   # result map for one paper.
    driver.get(url)   # open the url in the driver.
    if part[0] in citation: 
        ele = driver.find_element("xpath", "//button[@id='show-more-btn']")
        ele.click()
        author_elmts = driver.find_elements("xpath", "//div[@id='author-group']/a")
        ref_elmts = driver.find_elements("xpath", "//div[@id='author-group']/dl")
        ref_map = {}
        # get affiliation ref number map
        for index in range(len(ref_elmts)):
            rerf = ref_elmts[index]
            ref = rerf.find_element("xpath", "./dd").text
            try: title = rerf.find_element("xpath", "./dt/sup").text
            except Exception: title = str(index+1)
            ref_map[title] = ref

        # get author ref number map and find it in the affiliation map
        for index in range(len(author_elmts)):
            element = author_elmts[index]
            given_name = element.find_element("xpath", "./span/span[@class='text given-name']").text
            sur_name = element.find_element("xpath", "./span/span[@class='text surname']").text
            total_name = given_name + " " + sur_name
            try: 
                title_ref = element.find_element("xpath", "./span/span[@class='author-ref']").text
                author_ref_local[total_name] = ref_map[title_ref]
            except Exception:  # no author ref index specified.
                if (index < len(ref_elmts)): 
                    title_ref = str(index+1)
                    author_ref_local[total_name] = ref_map[title_ref]
                else: 
                    title_ref = "Unknown"
                    author_ref_local[total_name] = title_ref
            
    elif part[1] in citation:
        true_html_element = etree.HTML(rqs.get(url, headers=params).content)
        authors = true_html_element.xpath("//section[@class='core-authors']/div")
        for author in authors:
            given_name = author.xpath(".//span[@property='givenName']")[0].text
            surname = author.xpath(".//span[@property='familyName']")[0].text
            total_name = given_name + " " + surname
            organization = author.xpath(".//span[@property='name']")[0].text
            author_ref_local[total_name] = organization
    else:
        eles = driver.find_elements("xpath", "//a[@data-test='author-name']")
        # may have cookies on the above block the screen.
        try: driver.find_element("xpath","//button[@class='cc-button cc-button--contrast cc-banner__button cc-banner__button-accept']").click()
        except Exception: pass   
        # may have too many authors and some were hide, open the hide place.
        try: driver.find_element("xpath","//button[@class='c-button-author-list js-etal-show-more']").click()
        except Exception: pass
        # run the javascript to fetch affiliation
        # to avoid block the page, click again to hide.
        for i in eles:
            sleep(0.01)
            try: 
                i.click()
                i.click()
            except Exception: print("info: bad.")
        authors = driver.find_elements("xpath", "//h3[@class='c-author-popup__subheading']")
        for i in range(len(eles)):
            eles[i].click()
            author = authors[i]
            name = author.text
            organ = author.find_element("xpath", "./../ul/li").text
            author_ref_local[name] = organ
            eles[i].click()
    return author_ref_local



def crawler_main(x: pd.Series):
    """ The main crawler function. 

    Args:
        x (pd.Series): A row line in pandas.

    """
    # DOI number of files.
    DOI_url = x.DOI
    # use DOI to format primary url.
    url = "https://doi.org/" + DOI_url
    # use func toget the real url of the journal page
    html_url = get_redirection_url(x.Citation, url)
    # save the affiliation of the result into author.
    author_result = get_author_affiliation(x.Citation, html_url, driver)
    author_ref[DOI_url] = author_result


if __name__ == "__main__":
    df_ori = pd.read_excel("./Bik dataset - papers with endpoint reached.xlsx").iloc[33:,:]
    # run the main function of crawler
    df_ori.apply(crawler_main, axis=1)
    print(author_ref)
    # get the result down.
    with open("./result.json","w") as f:
        json.dump(author_ref,f)
