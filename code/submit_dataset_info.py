# script to easily have a standartised lookup of all datasets in the repo
# since descriptions might well contain commata, the resulting csv is tab-separated

from pandas import read_csv
import sys

if sys.version_info[0] < 3:
    raise Exception("Python 3 is required.")

# load old data so we can check for duplicates
# this try-except is horrible and needs to be replaced by a better way of dealing with paths
try:
    old_data = read_csv('../data/overview_of_datasets.csv', sep='\t')
    data_path = '../data/overview_of_datasets.csv'
except IOError:
    old_data = read_csv('data/overview_of_datasets.csv', sep='\t')
    data_path = 'data/overview_of_datasets.csv'

name = input('Name of the dataset:\n')
while name == '':
     print('Name required. Please try again.\n')
     name = input()

status = str(input('Status of the dataset, choose from\n 1: raw\n 2: preprocessed\n 3: integrated\n'))
while status not in ['1', '2', '3']:
    print('Status should be a number 1, 2, or 3. Please try again.\n')
    status = input()

if name in old_data.name.values and int(status) in old_data.status.values:
    print('A data set with this name and status already exists:')
    print(old_data[(old_data.name == name) & (old_data.status == int(status))])
    print('Please check that you are not submitting a duplicate and rerun the script.')
    exit(1)

source = input('Source of the dataset:\n')

description = input('Dataset description:\n')

license = input('Dataset license:\n')

other = input('Any other information about the dataset:\n')

csv_row = '\t'.join([name, status, source, description, license]) + '\n'
with open(data_path,'a') as f:
     f.write(csv_row)

print('Success!')

exit(0)