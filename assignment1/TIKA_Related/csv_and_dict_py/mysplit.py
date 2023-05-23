#!/usr/bin/python3 

import tika 
import argparse
import os

def main ():
    
    parser = argparse.ArgumentParser ()
    parser.add_argument ('-i', '--input_file', help='Input filepath', default='Bikdataset.csv')
    parser.add_argument ('-o', '--output_dir', help='Output directory', default='dataset')

    args = parser.parse_args () 
    for index, line in enumerate (open (args.input_file, 'rt')):
        if index == 0: continue # skip headers
        with open (os.path.join (args.output_dir, str (index) + '.csv'), 'wt') as fout:
            fout.write (line)



if __name__ == '__main__': main () 
