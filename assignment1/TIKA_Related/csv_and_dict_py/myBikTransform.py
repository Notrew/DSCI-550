#!/usr/bin/python3 

import tika 
import argparse
import os
import csv
def main ():
    
    parser = argparse.ArgumentParser ()
    parser.add_argument ('-i', '--input_file', help='Input filepath', default='Bikdataset.csv')
    parser.add_argument ('-o', '--output_file', help='Output directory', default='BikDataset.pyeval')

    args = parser.parse_args () 
    headers = []
    data = [] 
    for index, line in enumerate (csv.reader (open (args.input_file, 'rt'))):
        if index == 0: headers = line
        else: data.append (line)

    data_transformed = [] 
    for d in data:
        line_transformation = dict () 
        for i in range (0, len (headers)):
            if len (headers[i]) <= 0: continue
            key = headers [i]
            value = str (d [i].encode('utf-8').decode('utf-8').strip())
            line_transformation [key] = value
        data_transformed.append (line_transformation)
        
    with open (args.output_file, 'wt') as fout: 
        fout.write (str (data_transformed))


if __name__ == '__main__': main () 
