#!/usr/bin/env python

# This program can be used to combine a directory of MP3 files into a single
# file. The directory must be named in the following format:
# 2025-02-01_firstname-lastname_topic-discussed
# The program then sets the following mp3 tags:
# artist = Firstname Lastname
# album = 2025-02-01 Firstname Lastname Topic Discussed
# title = 2025-02-01 Firstname Lastname Topic Discussed
# recording date = 2025-02-01

# Install:
# python3
# pip install pydub
# pip install mutagen
# If Python 3.13 or newer, it may be necessary to: pip install audioop-lts

# To use:
# python <folder of MP3 files>

import os
from pydub import AudioSegment
import argparse
import eyed3
import re
import string

def parse_filename(filename):
    pattern = r"(\d{4}-\d{2}-\d{2})_(.+)_(.+)\.mp3"
    match = re.match(pattern, filename)
    if match:
        date, author, title = match.groups()
        author = author.replace("-", " ").title()
        title = title.replace("-", " ").title()
        return date, author, f"{date} - {author} - {title}"
    return None, None, None


def add_tags(file_path):
    audiofile = eyed3.load(file_path)
    if audiofile.tag is None:
        audiofile.initTag()

    filename = os.path.basename(file_path)
    date, author, album_title = parse_filename(filename)

    if author and album_title:
        audiofile.tag.artist = author
        audiofile.tag.album = album_title
        audiofile.tag.title = album_title
        audiofile.tag.recording_date = date
        audiofile.tag.save()

def merge_mp3_files(input_dir, output_file):
    # Get all MP3 files in the directory
    mp3_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.mp3')]
    
    if not mp3_files:
        print("No MP3 files found in the specified directory.")
        return
    
    # Sort the files alphabetically
    mp3_files.sort()
    
    # Initialize the merged audio
    merged_audio = AudioSegment.empty()
    
    # Merge all MP3 files
    for mp3_file in mp3_files:
        print("processing: ", mp3_file)
        file_path = os.path.join(input_dir, mp3_file)
        audio = AudioSegment.from_mp3(file_path)
        merged_audio += audio
    
    # Export the merged audio
    merged_audio.export(output_file, format="mp3")
    print(f"Merged {len(mp3_files)} MP3 files into {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple MP3 files in a directory into one file.")
    parser.add_argument("input_dir", help="Directory containing MP3 files")
    args = parser.parse_args()

    input_dir = args.input_dir.rstrip('/')
    output_file = input_dir.lower() + ".mp3"

    merge_mp3_files(input_dir, output_file)
    add_tags(output_file)
