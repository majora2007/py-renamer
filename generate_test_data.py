''' This script should be run on a directory which will generate a test case file 
    that can be loaded into the renametest.py'''
import os
root_dir = os.path.abspath('.')
current_folder = os.path.split(root_dir)[-1]
print(current_folder)

for root, dirs, files in os.walk(root_dir):
        with open(os.path.join(root_dir, current_folder + '-testcase.txt'), 'w+') as f:
            for file in files:
                 filename = os.path.join(root.replace(os.path.split(root_dir)[0] + '\\', ''), file)
                 f.write(filename + '\n')