#!/usr/bin/env python3
'''
This script get all interesting csv and merge without duplicates values
@author: Sotero Jr <http://soterojunior.github.io>
'''

from collections import OrderedDict
import os
from glob import iglob
import csv

# get all csv file in folder
files = sorted(iglob('*.csv'))
header = OrderedDict()
data = []

# Foreach all csv filename
for filename in files:
    with open(filename, 'r') as fin:
        csvin = csv.DictReader(fin)
        entries = [e for e in csvin]
        # Add the header the csv file
        header.update(OrderedDict.fromkeys(csvin.fieldnames))
        # List items in CSV
        for e in entries:
        	#if e in data:
        		# Check if item exists in array, it will not be added in array.
        		#print("Item Duplicate. Not Saved!")
        		#print(e["full_name"])
        	#else:
        		# Check if item there is not in array and add.
        		data.append(e)

# Write a new csv file with the items merged
with open('output_filename.csv', 'w', newline='') as fout:
    csvout = csv.DictWriter(fout, fieldnames=list(header))
    csvout.writeheader()
    csvout.writerows(data)


# Remove Duplicates subject in csv file
reader=csv.reader(open('output_filename.csv', 'r'), delimiter=',')
writer=csv.writer(open('output_without_duplicates.csv', 'w'), delimiter=',')

entries = set()

for row in reader:
   # column with subject name
   key = row[3] 
   # if there is not subject in entries, add in new csv, removing duplicates
   if key not in entries: 
      # Writing in new csv the subject
      writer.writerow(row)
      # Add subject name in entries to comparation
      entries.add(key)



print("Read Files:")
for filename in files:
	print(filename)