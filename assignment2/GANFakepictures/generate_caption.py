#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests

# Generate a list of img urls
data = pd.read_csv('img_urls.csv')
img_urls = data['urls'].to_list()

# Use docker to generate captions
captions = []
for i in range(len(img_urls)):
    url = "http://0.0.0.0:8764/inception/v3/caption/image?url=" + img_urls[i]
    res = requests.get(url).json()
    caption = res['captions'][0]['sentence']
    captions.append(caption)
    print(caption)

print(captions)

