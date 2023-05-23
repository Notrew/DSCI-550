#! /usr/bin/python3
# -*- encoding: utf-8 -*-

import os
from typing import List
from pylatex import Document, Section, Subsection, Command, Figure
from pylatex.utils import italic, NoEscape
import json
from random import randint

from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape


class MyDocument(Document):
    author: str
    name: str
    title: str
    def __init__(self, name, title, authors, publish_date):
        super().__init__(name)
        self.preamble.append(Command('title', title))
        self.preamble.append(Command('author', italic(authors)))
        self.preamble.append(Command('date', NoEscape(publish_date)))
        self.append(NoEscape(r'\maketitle'))
        self.author = authors
        self.name = name
        self.title = title


    def fill_document(self, text: List[str]):
        """Add a section, a subsection and some text to the document."""
        for para in text:
            section = para.split('.')[0]
            with self.create(Section(section)):
                self.append(para)

    def add_picture(self, pic: str, caption: str):
            with self.create(Figure(position='h!')) as kitten_pic:
                kitten_pic.add_image(pic, width='120px')
                kitten_pic.add_caption(caption)

def load_jsonl(path):
    data=[]
    with open(path, 'r', encoding='utf-8') as reader:
        for line in reader:
            data.append(json.loads(line))
    return data

def get_caption():
    with open("./caption_part1.csv","r") as f:
        f.readline()
        capture_list = f.read().strip("\n").split("\n")
    with open("./captionsaslist.list.csv","r") as g:
        raw = g.read()
        capture_list2 = eval(raw)
    return capture_list + capture_list2

if __name__ == '__main__':
    data = []
    jsonls = os.popen("ls *.jsonl").read().strip().split("\n")
    for i in jsonls:
        data += load_jsonl(i)
    tmp = {}
    captions = get_caption()
    count = 0
    print("Start Generating...")
    for article in data:
        print(f"\rProcessing: {count+1}/{len(data)} --> {(count+1)/len(data)*100:.2f}%",end='')
        # Document
        original_title = article["title"]
        article["title"]=article["title"].replace("/","_")
        article["title"]=article["title"].replace(".","_")
        article["title"]=article["title"].replace("%","_")
        article["title"]=article["title"].replace("\n"," ")
        article["title"]=article["title"].replace("\t"," ")
        article["title"]=article["title"].replace("\r"," ")
        article["title"]=article["title"].replace(":","_")
        article["title"]=article["title"].replace("@","_")
        article["title"]=article["title"].replace(";","_")
        article["title"]=article["title"].strip()
        doc = MyDocument(
            article["title"],article["title"], article["authors"],article["publish_date"]
        )

        # Call function to add text
        doc.fill_document(article["gens_article"])
        doc.add_picture(f"./generated_face/{count%500:03d}.png", captions[count%500])

        # Add stuff to the document
        doc.generate_tex(f'./tex/{article["title"]}')
        tmp[article["title"]] = (original_title, article["authors"])
        count += 1;
    print("\nfinished.")
