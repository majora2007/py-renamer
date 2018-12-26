import argparse
import commands
from episodeobj import EpisodeInfo
from episoderename import EpisodeRename
import os
import parse

from util import verbose, print_info

def get_argument(argument, default="None"):
	if argument:
		return argument[0]
	else:
		return default

def init_args():
    parser = argparse.ArgumentParser()
    # Required Parameters
    parser.add_argument('--show_name', required=True, nargs=1, help="Name of the Show. Will be used in rename")
    parser.add_argument('--season', required=False, nargs=1, help="Season for rename")

	# Optional Parameters
    parser.add_argument('--eps_per_file', required=False, nargs=1, help="Number of episodes per file")
    parser.add_argument('--dry', required=False, action='store_true', help="Perform a dry run. Does not perform a rename")
    parser.add_argument('--verbose', required=False, action='store_true', help="Detailed output")
    return parser.parse_args()

def find_subtitle(root_dir, filename):
    """ Walks a directory for a matching filename with subtitle extension. Returns None if no subtitles found """
    for _, _, files in os.walk(root_dir, topdown=True):
        for file in files:
            
            if parse.is_subtitle(file) and os.path.splitext(file)[0] == filename:
                return file
    return None

def info_has_parts(infos):
    for info in infos:
        if info.part_num > 0:
            return True
    return False

def generate_part_renames(infos):
    """ Uses a renamer suitable for handling files with parts (S01E01A -> S01E01, S01E01B -> S01E02). """
    return []

def generate_multiple_part_per_file_renames(infos):
    """ Uses a renamer suitable for handling files with Multiple Episodes contained within (S01E01 -> S01E01-E02). """
    return []

def generate_derived_season_renames(infos):
    """ Uses a renamer suitable for handling files with derived seasons. (Season 1 Episode 1 -> S01E01). """
    renames = []
    
    for info in infos:
        new_name = show_name + ' - ' + info.season + info.episode + ' - ' + info.title
        renames.append(EpisodeRename(info.original_filename, new_name))
    return renames

def generate_forced_season_renames(infos):
    """ Uses a renamer suitable for handling files by forcing a season on (Episode 1 -> S01E01). """
    return []

def generate_renames(infos):
    """ Given a list of EpisodeInfo objects, generate EpisodeRename objects using a renaming strategy best based on flags and metadata. """
    renames = []
    if info_has_parts(infos):
        print('Using Part Renamer')
        renames = generate_part_renames(infos)
    elif eps_per_file > 1:
        print('Using Multiple Episodes per File Renamer')
        renames = generate_multiple_part_per_file_renames(infos)
    elif season_num is None:
        print('Using derived season renamer')
        renames = generate_derived_season_renames(infos)
    else:
        print('Using standard renamer')
        renames = generate_forced_season_renames(infos)
    
    return renames


def generate_episode_infos(root_dir):
    file_infos = []
    for _, _, files in os.walk(root_dir, topdown=True):
        files.sort()
        for file in files:
            if parse.is_media_file(file):
                parts = os.path.splitext(file)
                filename = parts[0]
                info = EpisodeInfo(root_dir, filename)
                info.episode = parse.parse_episode(filename)
                info.part_num = parse.parse_episode_part(filename)
                info.subtitle = find_subtitle(root_dir, filename)
                info.extension = parts[1].replace('.', '')
                info.title = parse.parse_episode_title(filename)
                info.season = parse.parse_season(filename)
                file_infos.append(info)
    return file_infos

def write_renames(root_dir, renames):
    """ Responsible for renaming original files with standarized names """
    print('Updating files at {0}'.fromat(root_dir))
    for rename in renames:
        os.rename(os.path.join(root_dir, rename.original_filename), os.path.join(root_dir, rename.new_filename))

if __name__ == '__main__':
    # Required Args
    print_info('Parsing Arguments')
    args = init_args()
    show_name = str(get_argument(args.show_name))
    season_num = get_argument(args.season, None)
    if season_num is not None:
        season_num = int(season_num)

    # Optional 
    dry_run = bool(args.dry)
    eps_per_file = int(get_argument(args.eps_per_file, 1))
    verbose = bool(args.verbose)
    print('Verbose Mode: {0}'.format(verbose))


    #root_dir = os.path.abspath('.')
    root_dir = os.getcwd()
    file_infos = generate_episode_infos(root_dir)

    renames = generate_renames(file_infos)

    for rename in renames:
        print(rename)
    
    if not dry_run:
        print('Renaming files')
        write_renames(root_dir, renames)