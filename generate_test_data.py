''' This script should be run on a directory which will generate a test case file 
    that can be loaded into the renametest.py'''
import os
root_dir = os.path.abspath('.')

for _, _, files in os.walk(root_dir, topdown=True):
	with open(os.path.join(root_dir, root_dir + '-testcase.txt'), 'w') as f:
		for file in files:
			filename = os.path.splitext(file)[0]
			f.write(filename + '\n')