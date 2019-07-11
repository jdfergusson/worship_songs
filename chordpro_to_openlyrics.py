#!/usr/bin/python3

import argparse
import re

def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('in_song', metavar='INPUT_SONG', type=str)
    parser.add_argument('out_song', metavar='OUTPUT_SONG', type=str)
    
    return parser.parse_args()
    
args = get_args()

with open(args.in_song, 'r') as f:
    in_song = f.read()
    
r_title = re.match(r'\{?[tT]itle:([\w\s.,\']*)\}?', in_song)
titles = [t.strip() for t in r_title.groups()]





