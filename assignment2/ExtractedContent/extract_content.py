#!/usr/bin/env python
# coding: utf-8

import tika
tika.initVM()
from tika import parser
import json
import pandas as pd

# Read the csv file that lists pdf names
data = pd.read_csv('pdfs.csv')
pdfs = data['pdfs'].to_list()

# Use Tika to extract content
for pdf in pdfs:
    parsed = parser.from_file('./pdfs/' + pdf)
    content = parsed['content']
    content = content.replace('\n', '').strip()
    title = pdf.replace('.pdf', '')
    with open(title + '.json', 'w') as f:
        json.dump(content, f)

