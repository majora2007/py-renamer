''' This script should be run on a directory which will generate a test case file 
    that can be loaded into the renametest.py'''
import os
root_dir = os.path.abspath('.')

for dirpath, subdirs, files in os.walk(root_dir, topdown=True):
	with open(os.path.join(root_dir, root_dir + '-testcase.txt'), 'w') as f:
		for file in files:
			#filename = os.path.splitext(file)[0]
			filename = os.path.join(dirpath, file)
			f.write(filename + '\n')