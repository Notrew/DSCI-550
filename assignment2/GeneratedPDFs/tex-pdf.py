#! /usr/bin/python3
#
import json
import os

if __name__ == '__main__':
    file_list = os.popen("ls ./tex/*.tex").read().strip().split("\n")
    for f in file_list:
        value = os.system(f"pdflatex -enc -no-file-line-error -mltex '{f}'")
