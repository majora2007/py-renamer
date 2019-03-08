import re
from util import print_info

MEDIA_EXTENSIONS = ('.avi', '.mpeg', '.mp4', 'mkv', '.mpg', '.m4v')
SUBTITLE_EXTENSIONS = ('.srt')

EPISODE_NUM_REGEXS = [
    # show-season-1-episode-1
    re.compile(r'.*[-_]?season.{1}(?P<Season>\d+).{1}episode.{1}(?P<Episode>\d+)', re.IGNORECASE),
    # Episode 21 (no season)
    re.compile(r'(Episode\s)(?P<Episode>\d+)', re.IGNORECASE),
    # Happy Days 11-22 Fonzies Spots
    re.compile(r'(?P<Show>.*?)\s(\d{1,3})-(?P<Episode>\d+)', re.IGNORECASE),
    # Martin Mystery 201
    re.compile(r'(?P<Show>.*?)\s(\d{1})(?=[^\D])(?P<Episode>\d+)', re.IGNORECASE),
    # S01E01, E01, Episode 1, Show - S01E01, S01E01-E02
    re.compile(r'(?P<Show>.*?)(S{1}?\d+)(E|x)?(?P<Episode>\d+-?E?\d+)', re.IGNORECASE),
    # sabrinas-secret-life-2003-episode-1-at-the-hop
    re.compile(r'(?P<Show>.*)(\d{1,4})-(episode-)(?P<Episode>\d+).*', re.IGNORECASE),
    # 1x01, Show - 1x01, 1x01a
    re.compile(r'(?P<Show>.*?)(\d{1,3})x(?P<Episode>\d+)', re.IGNORECASE),
    # Happy Days 11-01
    re.compile(r'(?P<Show>.*?)(\d{1})-(?P<Episode>\d+)', re.IGNORECASE),
    # Ep1
    re.compile(r'(?P<Show>.*?)(Ep)?(?P<Episode>\d+)', re.IGNORECASE),
]

SEASON_REGEX = [
    # show-season-1-eps-1
    re.compile(r'.*[-_]?season.{1}(?P<Season>\d+)', re.IGNORECASE),
    # S01E01
    re.compile(r'(?P<Show>.*?)S(?P<Season>\d+)E?\d+.*', re.IGNORECASE),
    # 1x02
    re.compile(r'(?P<Show>.*?)(?P<Season>\d+)x\d+.*', re.IGNORECASE),
    # Happy Days 11-01 
    re.compile(r'(?P<Show>.*?)(?P<Season>\d+)-\d+.*', re.IGNORECASE),
    # sabrinas-secret-life-2003-episode-1-at-the-hop
    re.compile(r'(?P<Show>.*?)(?P<Season>\d{4}).*', re.IGNORECASE),
    # Martin Mystery 201
    re.compile(r'(?P<Show>.*?)(?P<Season>\d{1})(?P<Episode>\d+)', re.IGNORECASE)
]

EPISODE_PART_REGEXS = [
    # S01E01a - title (no leading characters)
    #re.compile(r'S\d+E\d+(?P<Part>[a-zA-Z]{1})', re.IGNORECASE),
    # E01a, 2x01a, Ep 1a, Epsiode 1a, Show - 1a
    re.compile(r'(.*)?\d+(?P<Part>[a-d]{1})', re.IGNORECASE)
]

EPISODE_TITLE_REGEX = [
    # Happy_Days_-_3-24_-_Arnold_s_Wedding_-_DVD2XviD
    re.compile(r'(?P<Show>.*?)[^season-]\d{1,3}-[^season-](?P<Episode>\d+)(?P<EpisodeTitle>.*)', re.IGNORECASE),
    # TMNT - S05E21 - Planet Of The Turtleoids Part 1
    re.compile(r'.*\d+[a-e]?(\s-\s)(?P<EpisodeTitle>.*)', re.IGNORECASE),
    # martin-mystery-episode-65-its-alive-part-1
    re.compile(r'.*(episode-\d+[a-e]?)(-)(?P<EpisodeTitle>.*)', re.IGNORECASE),
    # Generic
    re.compile(r'.*\d+[a-e]?(?P<EpisodeTitle>.*)', re.IGNORECASE)
]



def parse_season(filename):
    """ Attempts to parse Season from filename. If no season is found, returns S01. """
    print_info('Attempting to parse {0}'.format(filename))
    print_info('Extracting season from {0}'.format(filename))
    for regex in SEASON_REGEX:
        m = re.search(regex, filename)

        if m is None:
            continue

        extracted_season = m.group('Season').lower()
        print_info('Extracted season: {0}'.format(extracted_season))

        season_num = int(extracted_season)
        if season_num is not None and season_num > 0:
            print_info('Season might be: {0}'.format(season_num))
            return 'S' + format_num(season_num)
    return 'S01'

def parse_episode_title(filename):
    """ Attempts to parse episode title from filename. Will strip out separators at start of string. If no title is found, returns empty string"""
    print_info('Attempting to parse episode title from {0}'.format(filename))
    for regex in EPISODE_TITLE_REGEX:
        m = re.search(regex, filename)

        if m is None:
            continue

        extracted_title = m.group('EpisodeTitle')
        return clean_episode_title(extracted_title)
    return ''

def parse_episode_part(filename):
    """ Given a filename, attempts to match a part num (a = 1, b = 2) from the title. Returns 0 if no matches. """
    print_info('Extracting part num from {0}'.format(filename))
    baseline = ord('a')

    for regex in EPISODE_PART_REGEXS:
        m = re.search(regex, filename)

        if m is None:
            continue

        extracted_part = m.group('Part').lower()
        print_info('Extracted Part: {0}'.format(extracted_part))

        # Convert into int
        part_num = ord(extracted_part) - baseline + 1
        return part_num

    return 0

def parse_episode(filename):
    """ Given a filename, matches episode and returns episode in E01 format. This will ignore episode parts. Returns None if no matches."""
    print_info('Extracting episode from {0}'.format(filename))
    for regex in EPISODE_NUM_REGEXS:
        m = re.search(regex, filename)

        if m is None:
            continue

        extracted_ep = m.group('Episode').lower()
        print_info('Extracted episode: {0}'.format(extracted_ep))

        if '-' in extracted_ep:
            print_info('Multiple Episodes found')
            tokens = extracted_ep.split('-e')
            first_token = tokens[0]
            last_token = tokens[len(tokens)-1]
            return parse_episode(first_token) + '-' + parse_episode(last_token)
        else:
            ep_num = int(extracted_ep)
            if ep_num is not None and ep_num > 0:
                print_info('Episode might be: {0}'.format(ep_num))
                return 'E' + format_num(ep_num)

    return None

def clean_episode_title(filename):
    """ Removes special seperators like -,_  and leading spaces"""
    new_str = filename.replace('_', ' ').replace('-', ' ')
    return re.sub('\s+', ' ', new_str).strip()

def is_special_season(season_str):
    """ Returns True if Season is formated as Special (ie S00) """
    return season_str == 'S00'
    
def is_media_file(file):
    """ Returns true if file is a known media extension. This list is self-maintained. """
    return file.lower().endswith(MEDIA_EXTENSIONS)

def is_subtitle(file):
    """ Returns true if file is a known subtitle extension. This list is self-maintained. """
    return file.lower().endswith(SUBTITLE_EXTENSIONS)

def format_num(num):
    """ Formats a number to have leading 0 if below 10 """
    if num is None:
        return num
    if (num < 10):
        return '0' + str(num)
    return str(num)
 
if __name__ == '__main__':
    print('Hello')

