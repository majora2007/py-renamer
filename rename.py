import argparse
from episodeobj import EpisodeInfo
from episoderename import EpisodeRename
import os
import parse
import re


from util import verbose, print_info

anime_mode = False

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
    parser.add_argument('--season_maps', required=False, nargs=1, help="A set of episodes per season. ie) [2,2,1] -> S1 has 2 ep, S2 has 2 eps, S3 has 1")
    parser.add_argument('--anime', required=False, action='store_true', help='Use anime logic for reanming files. Keeps hashes and scene groups on rename.')
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
    renames = []
    highest_part = max(infos, key=lambda info: info.part_num).part_num
    print('highest part: {0}'.format(highest_part))
    for info in infos:
        episode_num = int(info.episode.split('E')[1])
        # (Ep_num - 1) * highest_part + part
        new_num = (episode_num - 1) * highest_part + info.part_num
        new_name = show_name + ' - ' + info.season + 'E' + parse.format_num(new_num) + ' - ' + info.title + '.' + info.extension
        renames.append(EpisodeRename(info.original_filename, new_name))
    return renames

def generate_multiple_part_per_file_renames(infos):
    """ Uses a renamer suitable for handling files with Multiple Episodes contained within (S01E01 -> S01E01-E02). """
    renames = []
    for info in infos:
        episode_num = int(info.episode.split('E')[1])
        end_num = episode_num*eps_per_file
        episode_seg = 'E' + parse.format_num(end_num-1) + '-E' + parse.format_num(end_num)
        new_name = show_name + ' - ' + info.season + episode_seg + ' - ' + info.title + '.' + info.extension
        renames.append(EpisodeRename(info.original_filename, new_name))

    return renames

def generate_derived_season_renames(infos):
    """ Uses a renamer suitable for handling files with derived seasons. (Season 1 Episode 1 -> S01E01). """
    renames = []
    
    for info in infos:
        if anime_mode:
            new_name = '[' + info.scene_group + '] ' + show_name + ' - ' + info.season + info.episode + ' - ' + info.title + ' ' + generate_media_info_format(info.media_info) + ' ' + info.hash_code + '.' + info.extension
        else:
            new_name = show_name + ' - ' + info.season + info.episode + ' - ' + info.title + '.' + info.extension
        renames.append(EpisodeRename(info.original_filename, new_name))
    return renames

def sum_until(arr, idx):
    """ Sums an array up until the index is reached. If you pass [1, 1], 1. The sum will be 1. """
    sum = 0
    for i, val in enumerate(arr):
        if i == idx:
            break
        sum += val
    return sum

def generate_season_map_file_renames(infos):
    """ Uses a renamer suitable for handling abs numbered files and splitting them into seasoned based on their number. """
    renames = []
    for info in infos:
        episode_num = int(info.episode.split('E')[1])
        bucket_index = 0
        sum = 0
        # Find what bucket episode_num fits in. We use +1 because 
        for idx, val in enumerate(season_maps):
            sum += val
            #print('Is {0} <= {1}'.format(episode_num, sum))
            if episode_num <= sum:
                print('Episode {0} maps to bucket {1} ({2} episodes)'.format(episode_num, idx, val))
                bucket_index = idx
                sum_until_bucket = sum_until(season_maps, idx)
                delta = abs(episode_num - sum_until_bucket)
                #print('Sum Until: {0}'.format(sum_until_bucket))
                #print('Delta: {0}'.format(delta))
                #episode_num = episode_num - delta
                episode_seg = 'E' + parse.format_num(delta)
                season_seg = 'S' + parse.format_num(bucket_index + 1)
                if anime_mode:
                    new_name = '[' + info.scene_group + '] ' + show_name + ' - ' + season_seg + episode_seg + ' - ' + info.title + ' ' + generate_media_info_format(info.media_info) + ' ' + info.hash_code + '.' + info.extension
                else:
                    new_name = show_name + ' - ' + season_seg + episode_seg + ' - ' + info.title + '.' + info.extension
                renames.append(EpisodeRename(info.original_filename, new_name))
                break
        
    return renames

def generate_media_info_format(media_info):
    """ Returns a formatted string from a media info object """
    if media_info.color_bits == '8':
        color_bits = ''
    else:
        color_bits = media_info.color_bits + '-bit'
    
    return '[{0}]'.format(re.sub(r' +', ' ', ' '.join([media_info.resolution, media_info.source, media_info.audio_source, color_bits, media_info.encoding])))

def generate_renames(infos):
    """ Given a list of EpisodeInfo objects, generate EpisodeRename objects using a renaming strategy best based on flags and metadata. """
    renames = []
    if info_has_parts(infos):
        print('Using Part Renamer')
        renames = generate_part_renames(infos)
    elif eps_per_file > 1:
        print('Using Multiple Episodes per File Renamer')
        renames = generate_multiple_part_per_file_renames(infos)
    elif len(season_maps) > 0:
        print('Using Season Maps Renamer')
        renames = generate_season_map_file_renames(infos)
    else:
        print('Using Derived Season Renamer')
        renames = generate_derived_season_renames(infos)
    return renames


def generate_episode_infos(root_dir):
    file_infos = []
    for _, _, files in os.walk(root_dir, topdown=False):
        files.sort()
        for file in files:
            if parse.is_media_file(file):
                parts = os.path.splitext(file)
                filename = parts[0]
                info = EpisodeInfo(root_dir, filename)
                info.original_filename = file
                if anime_mode:
                    info.episode = parse.parse_anime_episode(filename)
                    info.subtitle = find_subtitle(root_dir, filename) # TODO: See if this works fine for anime
                    info.extension = parts[1].replace('.', '')
                    info.media_info = parse.parse_media_info(filename)
                    info.title = parse.parse_anime_episode_title(filename)
                    info.hash_code = parse.parse_anime_hash(filename)
                    info.scene_group = parse.parse_anime_group(filename)
                    if season_num is None:
                        info.season = 'S01' # TODO: Figure out how to handle this. Assume Season 01 always? 
                    else:
                        info.season = 'S' + parse.format_num(int(season_num))
                else:
                    info.episode = parse.parse_episode(filename)
                    info.part_num = parse.parse_episode_part(filename)
                    info.subtitle = find_subtitle(root_dir, filename)
                    info.extension = parts[1].replace('.', '')
                    info.title = parse.parse_episode_title(filename)
                    #info.media_info = parse.parse_media_info(filename) # TODO: Implement test cases to handle for non-anime
                    if season_num is None:
                        info.season = parse.parse_season(filename)
                    else:
                        info.season = 'S' + parse.format_num(int(season_num))
                file_infos.append(info)
    return file_infos

def write_renames(root_dir, renames):
    """ Responsible for renaming original files with standarized names """
    print('Updating files at {0}'.format(root_dir))
    for rename in renames:
        if rename.original_filename == rename.new_filename:
            print('Skipping due to no rename needed, {0}'.format(rename.new_filename))
        else:
            os.rename(os.path.join(root_dir, rename.original_filename), os.path.join(root_dir, rename.new_filename))

# TODO: Remove this and declare it in tests...
global season_num
season_num = None

def parse_season_map(map_str):
    """ Parses an array from a str [1,2,3] """
    import ast
    return ast.literal_eval(map_str)


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
    anime_mode = bool(get_argument(args.anime, False))
    
    season_maps = parse_season_map(get_argument(args.season_maps, '[]'))
    if len(season_maps) > 0:
        print('Season Map: {0}'.format(season_maps))
    print('Verbose Mode: {0}'.format(verbose))
    print('Anime Mode: {0}'.format(anime_mode))


    root_dir = os.getcwd()
    file_infos = generate_episode_infos(root_dir)

    renames = generate_renames(file_infos)

    for rename in renames:
        print(rename)
    
    if not dry_run:
        print('Renaming files')
        write_renames(root_dir, renames)