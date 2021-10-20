#!/usr/bin/env python
import sys
import csv
import os

# Generate input CSV using:
# fc-list : -f "%{file}:%{family}:%{fullname}\n"
if len(sys.argv) < 3:
    sys.exit("usage: python fc-list.py IN.csv OUT.csv")

with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=':')

    fonts = []
    for row in csv_reader:
        filename = row[0].strip()
        _, ext = os.path.splitext(filename)
        if '.local/share/fonts' in filename:
            continue

        basename = os.path.basename(filename)
        family = row[1].strip().split(',')[0].strip()

        name = ''
        if len(row) >= 3:
            name = row[2].strip().split(',')[0].strip()
        if name == '':
            name = family

        fonts.append({
            'name': name,
            'family': family,
            'filename': basename,
        })

fonts.sort(key = lambda x: x['family'])
with open(sys.argv[2], 'wb') as csv_file:
    csv_writer = csv.writer(csv_file)
    for font in fonts:
        csv_writer.writerow([font['family'], font['name'], font['filename']])
