import os
root_dir = os.path.abspath('.')

def write_file(root_dir, filename):
	with open(os.path.join(root_dir, filename + '.txt'), 'w') as f:
		f.write('')

for _, _, files in os.walk(root_dir, topdown=True):
	for file in files:
		filename = os.path.splitext(file)[0]
		write_file(root_dir, filename)