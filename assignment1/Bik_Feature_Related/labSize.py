import json
from time import sleep
import requests as rqs
import pandas as pd
from lxml import etree
from typing import Dict, List

result_map: Dict[str, List[str]] = {}
params = {
    "cookie": "pm-csrf=5cLciDi3PGWIoOv32qDLfe8e8F0h4paCy06Mw086LibgvwgnCPdCCb3g50f3HCj1; ncbi_sid=103D822021157C53_21343SID; _ga=GA1.2.2019049496.1645312316; pm_ncbi_alert_dismiss=nCoV_shutdown; pm-sessionid=ayzagr2umb18y4kw84t3hpct1bip4n89; _gid=GA1.2.220341974.1646108647; pm-iosp=; recaptcha-ca-t=AW-bC4lozgOEFV64SD0X345L0dfXVBsdTmfeDF65rgywLrqMaQGBvDY5mz1AhMFVzP5wC2d45XRl8KD1sTn9LJi5XSV2lqqq3KuhdkEB3JqRxT-93TQVLM0jTAE1z-hyxZJCMxJuqAH1ADhM; pm-sfs=; _gat_ncbiSg=1; ncbi_pinger=N4IgDgTgpgbg+mAFgSwCYgFwgMIE4BMAHAAykCMAQgGICiZuVA7AKymkDMxAgg2exYwAiANnYA6MmIC2cdiAA0IAK4A7ADYB7AIaoVUAB4AXTKHyZwSgEZSo6RXKxgrNuyAAs5gM5QtEAMaI0J5KasaKzOYKIGRk5rGK+MTmeERslLT0TKxsnDxUfAIi4pIycgmxjs62GE7W1d6+AUEhhhgAcgDybTRR+GaVdahiKn6WyMNqUsPIiGIA5howvbhxzOzCUZzmhMIe9hXRaxv2/SA7eyDsDiAAZlpq3pseWIYQSlCbhJH2K1iE+Mw+lE3Ek/uw+BFFG5rsQxOxmGIklDnsp1NpdAYwu4IlgkSA1uZcIQLswUYwyF9whssDEosxGOZhMcQMIDm4yHimV4fP5ECAAL78oA==",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98";',
    "sec-ch-ua-platform": "Windows",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
}
# Use to indicates progress at console.
progress = 0  
shape = 0  

def craw_artical_page(html: etree._Element, name: str) -> bool:
    """Get author info from PubMed Artical page

    Args:
        html (etree._Element): HTML Element
        name (str): author name

    Returns:
        bool: _description_
    """
    global result_map;
    author_list = html.xpath("//div[@class='full-view']//a[@class='full-name']/text()")
    result_map[name].extend([i.strip().strip(",") for i in author_list])
    return True

def craw_search_page(html: etree._Element, name: str, univ: str, flag:bool) -> bool:
    """Get Authors Info from PubMed Search Page.

    Args:
        html (etree._Element): html_element
        name (str): author_name
        univ (str): author_affiliation
        flag (bool): avoid name collision

    Returns:
        bool: whether to stop crawl info of the author.
    """
    global result_map;
    page_num_max = html.xpath(".//input[@id='page-number-input']/@max")[0]
    page_num_now = html.xpath(".//input[@id='page-number-input']/@value")[0]
    # To avoid chinese name's collision
    if (int(page_num_max)>=50) and not flag:  
        return auto_crawler(name, univ, 1)  # Must be True
    print(f"\r    page: {page_num_now}/{page_num_max}",end='')
    article_author_list = html.xpath(".//span[@class='docsum-authors full-authors']")
    for article in article_author_list:
        author_str = "".join(
            article.xpath("./text()") + article.xpath("./*/text()")
        )
        author_str = author_str.strip().strip(".")
        result_map[name].extend([i.strip() for i in author_str.split(",")])
    return page_num_max == page_num_now


def auto_crawler(name: str, university: str, flag:bool) -> int:
    """The main crawler function.

    Args:
        name (str): author_name
        university (str): author_affiliation
        flag (bool): too much name collision

    Returns:
        int : count
    """
    global params, result_map
    page_num = 1
    result_map[name] = []
    count : int
    while True:
        url = f"https://pubmed.ncbi.nlm.nih.gov/?term={name} {university if flag else ''}&page={page_num}"
        response = rqs.get(url, headers=params)
        html: etree._Element = etree.HTML(response.content)
        search_page: List[etree._Element] = html.xpath("//main[@id='search-page']")
        article_page: List[etree._Element] = html.xpath("//main[@id='article-details']")
        if (# when the results are search pages:
            len(search_page)
            and craw_search_page(search_page[0], name, university, flag)
            # when there is only one article, it will redirect to the artical page:
            or len(article_page) 
            and craw_artical_page(article_page[0], name)
        ):
            count = set(result_map[name]).__len__()
            break
        else:
            page_num += 1
        # Sleep to avoid 403 forbidden, and 503 sevices unavailiable
        sleep(0.1)   
    return count


def main_iter_func(auth: pd.Series):
    global progress
    progress += 1
    author_name: str = auth.fa
    university: str = auth.University
    print(f"\nprogress: {progress/shape*100:.2f}% --> {progress}/{shape} : {author_name}")
    return auto_crawler(author_name, university, 0)


if __name__ == "__main__":
    df = pd.read_excel("./Bik dataset - papers with endpoint reached.xlsx")
    shape = df.shape[0]   # use to indicates progress
    df.rename({"First Author": "fa"},axis=1,inplace=True)
    df["count_total"] = df[["fa","University"]].apply(main_iter_func, axis=1)
    df.to_excel("./Bik_result.xlsx")
    with open ("author_list.json","w") as f:
        json.dump(result_map, f)
    
    
