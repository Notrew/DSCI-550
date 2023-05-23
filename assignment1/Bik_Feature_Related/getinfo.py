#request
#BeautifulSoup
import requests
from bs4 import BeautifulSoup
import json
import pandas
import os

def main():
	#input url
    url1 = ["https://pubmed.ncbi.nlm.nih.gov/20636343/",
    "https://pubmed.ncbi.nlm.nih.gov/19170727/",
    "https://pubmed.ncbi.nlm.nih.gov/22498339/",
    "https://pubmed.ncbi.nlm.nih.gov/22640257/",
    "https://pubmed.ncbi.nlm.nih.gov/15107539/",
    "https://pubmed.ncbi.nlm.nih.gov/15781995/",
    "https://pubmed.ncbi.nlm.nih.gov/20840156/",
    "https://pubmed.ncbi.nlm.nih.gov/22563695/",
    "https://pubmed.ncbi.nlm.nih.gov/20167112/",
    "https://pubmed.ncbi.nlm.nih.gov/23701827/",
   
    ]
    
    
    
    author_info = []
    info={}
    dirname = 'htmls'
    #os.mkdir (dirname)
    for i in url1: 
        # save to directory if not previously downloaded
        paper_id = i.split ('/')[-2]
        filepath = os.path.join (dirname, paper_id + '.html')
        if not os.path.isfile (filepath):
            response = requests.get(i)
            #print(response.text)#print the raw source
            with open (filepath, 'wt') as fout: 
                fout.write (response.text)

        htmltext = open (filepath, 'rt').read () 
        main_page = BeautifulSoup(htmltext, "html.parser")
        Type_list = main_page.find("li", attrs = {"data-affiliation-id":"affiliation-1"})#find "span" and attrs by clicking right mouse on the content and go to "inspect"
        name = main_page.find("h1",attrs = {"class":"heading-title"}).text
        info[name.replace('\n','').strip ()[1]] = Type_list.text
        author_info.append(Type_list.text)
    country = []   
    university = []
    l_of_output= author_info
   
    if False: 
        #find the index of commas and dots
        country = []
        commas_i= []
        dots_i = []
        #for every author info in the total author_info list
        for one_line in l_of_output:
            #for every digit's index in every author info
            for index in range(len(one_line)):
                if one_line[index] == ",": 
                    commas_i.append(index)#all commas index
                if one_line[index] == ".":
                    dots_i.append(index)#all dots index
            find_commas = []
            
            first_d = dots_i[0]
            #find the comma'index before the first dot
            for c in commas_i:
                if c < first_d:
                    find_commas.append(c)
            comma = find_commas[-1]+2
        
            country.append(one_line[comma:first_d])
    else:  
        country = [] 
        for one_line in l_of_output:
            print (one_line, end='\033[92m ----> \033[0m')
            one_line = one_line [: one_line.find ('.')]
            one_line = one_line [one_line.rfind (',')+1: ]
            one_line = one_line.strip () 
            print ('\033[91m'+one_line+'\033[0m')
            country.append (one_line)
    print(country)
    
    #get university data
    university = [] 
    for one_line in l_of_output:
        print (one_line, end='\033[92m ---> \033[0m')
        items = one_line.split (',')
        for item in items:
            item = item.strip () 
            if 'Univers' in item or 'College' in item: 
                university.append (item)
                print ('\033[91m'+item+'\033[0m')
    print (university)
      
    #get department data
    department = []
    for one_line in l_of_output:
        items = one_line.split(',')
        print (one_line, end='\033[92m ---> \033[0m')
        for item in items:
            item = item.strip()
            if 'Department' or 'department' in item:
                department.append(item)
                print ('\033[91m'+item+'\033[0m')

    print(department)
    #print(info)
    #print(json.dumps (info, indent=4))
    
if __name__ == "__main__":
    main()   
    
