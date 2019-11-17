#!/usr/bin/env python
import sys
import csv
import os
import shutil

def generate_md(path, os, fonts):
    with open(path, 'w') as file:
        # Write operating system heading.
        file.write('## %s\n\n' % os)

        # Write table header.
        file.write('| Family | Name | Filename |\n')
        file.write('| :--- | :--- | :--- |\n')

        # Write font rows.
        for f in fonts:
            file.write('|%s|%s|%s|\n' % (f['family'], f['name'], f['filename']))

if __name__== "__main__":
    # Get current directory.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if not current_dir:
        sys.exit('could not get location of current directory')

    md_dir = os.path.join(current_dir, 'md')
    if os.path.exists(md_dir):
        shutil.rmtree(md_dir)

    csv_dir = os.path.join(current_dir, 'csv')
    for os_dir in os.listdir(csv_dir):
        os_dir_path = os.path.join(csv_dir, os_dir)
        for csv_file in os.listdir(os_dir_path):
            # Read font CSV file.
            with open(os.path.join(os_dir_path, csv_file)) as file:
                csv_reader = csv.reader(file, delimiter=',')

                fonts = []
                for row in csv_reader:
                    fonts.append({
                        'family': row[0].strip(),
                        'name': row[1].strip(),
                        'filename': row[2].strip()
                    })

                # Sort fonts.
                fonts = sorted(fonts, key = lambda x: (x['family'], x['name']))

            # Create Markdown directories.
            md_os_dir = os.path.join(md_dir, os_dir)
            if not os.path.exists(md_os_dir):
                os.makedirs(md_os_dir)

            # Generate Markdown file.
            md_filename = os.path.splitext(csv_file)[0]
            md_file = os.path.join(md_os_dir, md_filename+'.md')
            os_name = md_filename.replace('-', ' ').replace('_', ': ')
            generate_md(md_file, os_name, fonts)
