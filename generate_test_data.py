''' This script should be run on a directory which will generate a test case file 
    that can be loaded into the renametest.py'''
import os
from pathlib import Path


def create_test_base(file, root_dir):
    ''' Creates and returns a new base directory for data creation for a given testcase.'''
    base_dir = os.path.split(file.split('-testcase.txt')[0])[-1]
    print('base_dir: {0}'.format(base_dir))
    new_dir = os.path.join(root_dir, base_dir)
    p = Path(new_dir)
    if not p.exists():
        os.mkdir(new_dir)

    return new_dir



def generate_data(file, root_dir):
    ''' Generates directories and fake files for testing against '''

    if file.endswith('-testcase.txt'):    
        base_dir = create_test_base(file, root_dir)
    
    """ files_to_create = []
    with open(file, 'r') as in_file:
        files_to_create = in_file.readlines() """
    
    for part in os.path.split('Mythbusters\Season 01\Mythbusters s01e02 - Airplane Toilet, Biscuit Bazooka, Leaping lawyer.avi'):
        p = pathlib.Path(part)
        if not p.exists():
            print('make {0}'.format(part))

    """ for f in files_to_create:
        path_parts = os.path.split(f) """

def generate_test_file():
    root_dir = os.path.abspath('.')
    current_folder = os.path.split(root_dir)[-1]
    out_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if not file.endswith('-testcase.txt'):
                filename = os.path.join(root.replace(os.path.split(root_dir)[0] + '\\', ''), file)
                out_files.append(filename)
            else:
                print('root: {0}'.format(root))
                print('file: {0}'.format(file))
                print('root_dir: {0}'.format(root_dir))

    with open(os.path.join(root_dir, current_folder + '-testcase.txt'), 'w+') as f:
        for filename in out_files:
            f.write(filename + '\n')

if __name__ == '__main__':
    #generate_test_file()
    filepath = os.path.join(os.path.abspath('./tests/cases/'), 'Mythbusters-testcase.txt')
    generate_data(filepath, os.path.abspath('./tests/cases/'))