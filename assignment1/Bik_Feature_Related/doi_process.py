import requests
import os


from bs4 import BeautifulSoup
def main():
    doi_file ='doi.csv' 
    dirname = 'paperhtml'
    for line in open (doi_file, 'rt'): #process and clean doi.csv line by line
        if line.startswith ('PMID: '):
            pmid = line [6: ].strip ()
            url = "https://pubmed.ncbi.nlm.nih.gov/"+pmid
            filepath = os.path.join (dirname, 'pmid-'+pmid+'.html')
        else: 
            doi = line.strip () 
            url = "https://pubmed.ncbi.nlm.nih.gov/?term="+ str(doi) + "%5BLocationID%5D&sort="
            filepath = os.path.join(dirname, doi.replace ('/', '_') + '.html') 
        if not os.path.isfile(filepath):
            response = requests.get(url) #send request to the web
            if response.ok:
                with open(filepath,'wt') as fout:
                    fout.write(response.text) 
        if os.path.isfile (filepath): 
            htmltext = open(filepath, 'rt').read () #read the text in html
            mainpage = BeautifulSoup(htmltext, "html.parser") #parse html
            fulltextsources = {} #the final output of all other journals published in
            try:
                textsources = mainpage.find("ul", attrs = {"class":"linkout-category-links"}).text 
                textsources = textsources.replace("\n",'')
                textsources = textsources.replace("                                     ",',').strip()
                fulltextsources[doi] = textsources
            except Exception:
                pass
        print(fulltextsources)
             
if __name__ == "__main__":
    main()
