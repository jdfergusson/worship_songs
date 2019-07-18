#!/usr/bin/python3

import argparse
import re
import json
import os
import subprocess

notes = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab']

def get_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('song_list', type=str, help="json file containing songname and key pairs")
    parser.add_argument('output_file', type=str, help="Output PDF file")
    parser.add_argument('--chords_dir', type=str, help="Folder containing chordpro files", default="chords/")
    parser.add_argument('--settings_file', type=str, help="JSON file of chordpro settings", default="chordpro_settings.json")
    
    return parser.parse_args()
    
args = get_args()

with open(args.song_list, 'r') as f:
    song_list = json.load(f)
    
out_files = []
    
for song in song_list:
	song_file = os.path.join(args.chords_dir, song['file'])
	with open(song_file, 'r') as f:
		song_data = f.read()
		
	search = re.search(r'\{[Kk]ey: ?\[?([A-G][b#]?)\]?\}', song_data)
	if not search:
		print('Failed to get key for {}'.format(song))
		continue
		
	current_key = notes.index(search.group(1))
	target_key = notes.index(song['key'])
	capo = song['capo']
	
	transpose_delta = target_key - current_key
	if transpose_delta < 0: 
		transpose_delta += 12
	
	# Replace title
	r = re.compile(r'\{[Tt]itle: ?([A-Za-z0-9\'",-_/\(\) ]*)\}')
	search = r.search(song_data)
	if not search:
		print('Failed to get title for {}'.format(song['file']))
		continue
	title = search.group(1)
	title += ' - {}'.format(notes[target_key])
	title += ' (capo {})'.format(capo) if capo != 0 else ''
	song_data = r.sub('{{title: {}}}'.format(title), song_data)
	
	# Write edited file to temp
	modifiable_file_path = os.path.join('/tmp', os.path.split(song['file'])[-1]) + '_{}_{}.pro'.format(target_key, capo)
	with open(modifiable_file_path, 'w') as f:
		f.write(song_data)
		
	pdf_out_file = modifiable_file_path + '.pdf'
	out_files.append(pdf_out_file)
		
	cmd = 'chordpro {infile} --output {outfile} -G ' \
		'--config={configfile} --transpose {transpose}'.format(
			infile=modifiable_file_path,
			outfile=pdf_out_file,
			configfile=args.settings_file,
			transpose=transpose_delta,
		)
		
	subprocess.run(cmd.split(' '))
	
if out_files:
	subprocess.run(['pdfunite'] + out_files + [args.output_file])
			
		
		

