# 

# Test Cases: 
# Codename.Kids.Next.Door.S01E13.Operation.I-S.C.R.E.A.M.-.Operation.C.A.N.N.O.N.480p.WEB-DL.AAC2.0.H.264-SA89
# Cow and Chicken - 101 - Foo bar
# Braceface 1x05 Episode Title
# Braceface 1x05a Episode Title

import re
import os
import argparse
import commands


def get_argument(argument, default="None"):
	if argument:
		return argument[0]
	else:
		return default


def proper_episode_format(count):
	if count < 10:
		return '0'+str(count)
	return str(count)

def extract_season(number):
	#if str(number).startswith('0'):
	#    return str(number)[0:2]
	#else:
	#    try:
	#        return str(number)[0:str(number).index('E')]
	#    except:
	#        pass
		
	return season

def episode_has_parts(name): 
	m = re.search(PART_REGEX, name)
	if m is None:
		if separator in name:
			return True
		return False

	return True

def get_episode_part(name):
	m = re.search(PART_REGEX, name)
	if m is None:
		return None

	return m.group('Part')

def is_special(name, nums):
	# Extract numbers out of the file
	return str(filenum).startswith('00')
	#return False

def extract_episode(number, season):
	# This transforms a complete number (ie 111) into a string of just the episode (11). Else just returns episode if already proper
	number = str(number)
	print('number: {0}'.format(number))
	# TODO: Need to handle episodes that spawn 2 numbers
	just_episode = number
	if number.startswith(str(season)):
		just_episode = number[len(str(season)):]
	if '-' in str(just_episode):
		print(just_episode)
	
	# print('S' + season + 'E' + number + ' -> ' + just_episode)
	return proper_episode_format(int(number))

def init_args():
	parser = argparse.ArgumentParser()

	# Required Parameters
	parser.add_argument('--show_name', required=True, nargs=1, help="Name of the Show. Will be used in rename")
	parser.add_argument('--season', required=True, nargs=1, help="Season for rename")

	# Optional Parameters
	parser.add_argument('--eps_per_file', required=False, nargs=1, help="Number of episodes per file")
	parser.add_argument('--dry', required=False, action='store_true', help="Perform a dry run. Does not perform a rename")
	parser.add_argument('--extra_separators', required=False, nargs=1, help="Number of extra -'s in file for counting parts if applicable")
	parser.add_argument('--separator', required=False, nargs=1, help="A string that acts as a separator. ie) - or .-.")

	return parser.parse_args()


class EpisodeInfo(object):
	root_dir = ''
	filename = ''
	extension = ''
	episode_num = -1
	part_num = -1
	orig_filename = ''
	subtitle = ''
	title = '' # Represents rest of the filename
	def __init__(self, root_dir, filename):
		self.root_dir = root_dir
		self.filename = filename

	def __str__(self):
		return '[filename] ' + self.filename + ', [extension] ' + self.extension + ', [episode_num] ' + self.episode_num + ', [part_num] ' + self.part_num


def find_episode_info(infos, filenum):
	for info in infos:
		if info.episode_num == filenum:
			return info
	return None

args = init_args()

print("Parsing Arguments")

# Required Arguments
show_name = str(get_argument(args.show_name))
season = str(get_argument(args.season))

# Optional Arguments
dry_run = bool(args.dry)
eps_per_file = int(get_argument(args.eps_per_file, 1))
extra_separators = int(get_argument(args.extra_separators, 0))
separator = str(get_argument(args.separator, '-'))


print("Finished Parsing Arguments")
print('Dry Run: {0}'.format(dry_run))
root_dir = os.path.abspath('.')
counter = 1
extension = ('.avi', '.mpeg', '.mp4', 'mkv', '.mpg', '.m4v')
print('root dir: {0}'.format(root_dir))
print('\n')

infos = []
# We need to covert these Regex into an array of possible matches and return the first match back. 
PART_REGEX = re.compile(r'(?P<Episode>\d+)(?P<Part>[a-d]{1})') # OLD (-|\d+\B)(\D{1})\b
EPISODE_NUM_REGEX = re.compile(r'(?P<Episode>\d{1,3}(?!\d+|(?:[ex]|\W[ex]|_|-){1,2}\d+))(?P<Part>[a-d]{1})?(?P<Title>.*)') ### OLD: [^S\d+](?P<Episode>\d+)
EPISODE_REPLACE_REGEX = re.compile(r'S?\d+([x-]?\D?)')
FILENAME_REPLACE_REGEX = re.compile(r'^\D*[\s.]{1}S?\d+[x|e|-]?\d*\D?[0-9]*')

# This critically requires to find the episode files in correct order
for root, dirs, files in os.walk(root_dir, topdown=True):
	files.sort()
	for file in files:
		if file.lower().endswith(extension):
			fileparts = os.path.splitext(file)
			# I need to ignore anything that is surrounded in [], used spaces 
			filename = fileparts[0]
			match = re.search(EPISODE_NUM_REGEX, filename)
			print(filename)
			filenum = match.group('Episode')
			
			#season = extract_season(filenum)
			if is_special(filename, filenum):
				continue

			# To ensure we are in order processing, let's pack the episodes into an array and process later
			info = EpisodeInfo(root_dir, filename)
			info.episode_num = extract_episode(filenum, season)
			info.extension = fileparts[1]
			info.orig_filename = file
			info.title = match.group('Title')

			if episode_has_parts(filename):
				end_part = get_episode_part(filename)
				if end_part is not None and end_part.isalnum():
					info.part_num = ord('a') - ord(end_part)
				else:
					info.part_num = filename.count(separator) - extra_separators + 1 # We add 1 because 1 separator means Ep 1 - Ep 2. 
			infos.append(info)


for root, dirs, files in os.walk(root_dir, topdown=True):
	files.sort()
	for file in files:
		if file.lower().endswith('.srt'):
			fileparts = os.path.splitext(file)
			# I need to ignore anything that is surrounded in [], used spaces 
			filename = fileparts[0]
			match = re.search(EPISODE_NUM_REGEX, file)
			info = find_episode_info(infos, extract_episode(filenum, season))
			if info:
				info.subtitle = file

#TODO: Ensure files are sorted by filenum then filepart (if > -1)


counter = 1
current_ep_num = infos[0].episode_num
for info in infos:
	episode_part = 'E' + proper_episode_format(counter)
	#print('counter: ' + str(counter))
	if eps_per_file > 1:
		episode_part = episode_part + '-E' + proper_episode_format(counter + eps_per_file - 1)
		counter = counter + eps_per_file
	elif info.part_num > 1 and eps_per_file is not 1:
		print('Naming with ' + str(info.part_num) + ' episodes per file.')
		episode_part = episode_part + '-E' + proper_episode_format(counter + info.part_num - 1)
		counter = counter + info.part_num
	else:
		counter = counter + 1

	show_part = show_name + ' - ' 
	
	#filename = show_part + re.sub(FILENAME_REPLACE_REGEX, 'S' + proper_episode_format(int(season)) + episode_part + ' ', info.filename) + info.extension
	filename = show_part + 'S' + proper_episode_format(int(season)) + episode_part + ' - ' + info.title + info.extension
	print(info.orig_filename)
	print('\t\t -> ' + filename)
	if info.subtitle:
		subtitle = show_part + 'S' + proper_episode_format(int(season)) + episode_part + ' - ' + info.title + info.extension + '.srt'
		print('\t\t -> ' + subtitle)
	if not dry_run:
		os.rename(os.path.join(info.root_dir, info.orig_filename), os.path.join(info.root_dir, filename))
		if info.subtitle:
			os.rename(os.path.join(info.root_dir, info.subtitle), os.path.join(info.root_dir, subtitle))