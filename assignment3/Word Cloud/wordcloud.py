#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# In[34]:


f = open("./entity_json/fox.json","r")
data = json.loads(f.read())
keys=list(data.keys())


# In[ ]:


def catch_value(file_name, value, position):
    f = open(file_name, encoding='utf-8')
    setting = json.load(f) 
    f.close()
    my_value = setting[position][value]  
    return my_value


# In[ ]:


if __name__ == '__main__':
    file=open("./wordcloud/fox_product.txt",'a');
    for i in keys:
        cat = catch_value("./entity_json/fox.json", "PRODUCT", i)
#         print(type(nationality1))
        for j in cat:
            print(j)
            file.write(j+'\n')
    file.close()
    print("ok")


# In[ ]:


f = open('./wordcloud_file/product.txt','r',encoding='utf-8').read()
wordcloud = WordCloud(
        background_color="white", 
        width=1500,              
        height=960,              
        margin=10               
        ).generate(f)

plt.imshow(wordcloud)

plt.axis("off")

plt.show()

wordcloud.to_file('./wordcloud_pic/product.png')

