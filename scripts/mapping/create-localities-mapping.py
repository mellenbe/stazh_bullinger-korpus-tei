#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import csv
import xml.etree.ElementTree as ET

LETTERS_PATH = 'data/letters'
OUTPUT_PATH = 'data/mapping/localities-mapping.csv'

# Dictionary to store place reference counts
place_counts = {}

# Iterate over all XML files in the letters directory
for filename in os.listdir(LETTERS_PATH):
    if filename.endswith('.xml'):
        file_path = os.path.join(LETTERS_PATH, filename)
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

            # Use sets to ensure each place is only counted once per category per letter
            corresp_set = set()
            mention_set = set()

            # Collect places from correspDesc
            for place in root.findall('.//tei:teiHeader//tei:correspDesc//tei:placeName', ns):
                ref = place.attrib.get('ref', '').lstrip('#')
                if ref:
                    corresp_set.add(ref)

            # Collect places from main text
            for place in root.findall('.//tei:text//tei:placeName', ns):
                ref = place.attrib.get('ref', '').lstrip('#')
                if ref:
                    mention_set.add(ref)

            # Update the counts, once per category per letter
            for ref in corresp_set:
                place_counts.setdefault(ref, {'corresp': 0, 'mentions': 0})
                place_counts[ref]['corresp'] += 1

            for ref in mention_set:
                place_counts.setdefault(ref, {'corresp': 0, 'mentions': 0})
                place_counts[ref]['mentions'] += 1

        except ET.ParseError:
            print(f"Error while parsing {filename}")

# Write results to CSV file
with open(OUTPUT_PATH, mode='w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['placeID', 'corresp', 'mentions'])
    for place_id, counts in sorted(place_counts.items()):
        writer.writerow([place_id, counts['corresp'], counts['mentions']])

print(f"Successfully generated CSV file: {OUTPUT_PATH}")
