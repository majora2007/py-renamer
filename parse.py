import re
from util import print_info
from mediainfo import MediaInfo

MEDIA_EXTENSIONS = ('.avi', '.mpeg', '.mp4', 'mkv', '.mpg', '.m4v', '.mpeg')
SUBTITLE_EXTENSIONS = ('.srt', '.ass')
MANGA_EXTENSIONS = ('.cbz', '.cbr', '.zip', '.rar', '.epub')

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
    # s1ep2
    re.compile(r'(?P<Show>.*?)(Ep)(?P<Episode>\d+)', re.IGNORECASE),
    # Ep1
    re.compile(r'(?P<Show>.*?)(Ep)?(?P<Episode>\d+)', re.IGNORECASE),
]

SEASON_REGEX = [
    # show-season-1-eps-1
    re.compile(r'.*[-_]?season.{1}(?P<Season>\d+)', re.IGNORECASE),
    # S01E01
    re.compile(r'(?P<Show>.*?)S(?P<Season>\d+)E?\d+.*', re.IGNORECASE),
    # S01EP01
    re.compile(r'(?P<Show>.*?)S(?P<Season>\d+)(EP)?\d+.*', re.IGNORECASE),
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
    # BBC.Natures.Microworlds.01of13.Galapagos.720p.HDTV.x264.AAC.MVGroup.org
    re.compile(r'\d+((of)[a-e]?)(\d+)?(?P<EpisodeTitle>.*)', re.IGNORECASE),
    # Generic
    re.compile(r'.*\d+[a-e]?(?P<EpisodeTitle>.*)', re.IGNORECASE)
]

ANIME_HASH_REGEXS = [
    re.compile(r'(?P<Hash>\[.{8}\])', re.IGNORECASE)
]

ANIME_GROUP_REGEXS = [
    re.compile(r'\[(?P<Group>[A-Z]+)\]', re.IGNORECASE)
]

ANIME_EPISODE_NUM_REGEXS = [
    re.compile(r'_(?P<Episode>\d+)(v\d)?_', re.IGNORECASE), # _(?P<EpisodeTitle>\d*[\w_(\-\b)?!]*)-?_\d
    # Not Hi10, not resolution.
    re.compile(r'[^Hi](?P<Episode>\d+)(v\d)?[^p\)\]]', re.IGNORECASE)
]

ANIME_EPISODE_TITLE_REGEXS = [
    # [CBM]_Gurren_Lagann_-_01_-_Bust_Through_the_Heavens_With_Your_Drill!_[720p]_[D2E69407].mkv
    re.compile(r'(?:_-_)(?P<EpisodeTitle>[a-z_!\',]*)_', re.IGNORECASE)
]
 
MEDIA_INFO_RESOLUTION_REGEXS = [
    # [UTW]_Accel_World_-_01_[h264-720p][7A2BE7A5].mkv
    re.compile(r'(\(?\[?){1}(?P<MediaInfo>\d{3,4})(p).*', re.IGNORECASE),
    # (1280x720 or [720p]
    re.compile(r'(\(?\[?){1}(?P<MediaInfo>\d{3,4})(p|x)?.*', re.IGNORECASE)    
]

MEDIA_INFO_SOURCE_REGEXS = [
    # [Coalgirls]_Ro-Kyu-Bu!_SS_01_(1280x720_Blu-Ray_FLAC)_[E1AC4C4A].mkv
    re.compile(r'(\(?\[?){1}(?P<MediaInfo>Blu-Ray).*', re.IGNORECASE),
    # [Doki]_30-sai_no_Hoken_Taiiku_-_01v2_(1280x720_h264_BD_AAC)_[F9915E0F].mkv
    re.compile(r'(\(?\[?){1}(?P<MediaInfo>BD).*', re.IGNORECASE),
    # BDRip
    re.compile(r'(\(?\[?){1}(?P<MediaInfo>BDRip).*', re.IGNORECASE),
    # HDTV
    re.compile(r'(\(?\[?){1}(?P<MediaInfo>HDTV).*', re.IGNORECASE) 
]

MEDIA_INFO_AUDIO_SOURCE_REGEXS = [
    # [Coalgirls]_Ro-Kyu-Bu!_SS_01_(1280x720_Blu-Ray_FLAC)_[E1AC4C4A].mkv
    re.compile(r'(\(?\[?){1}(?P<MediaInfo>FLAC).*', re.IGNORECASE),
    # [Doki]_30-sai_no_Hoken_Taiiku_-_01v2_(1280x720_h264_BD_AAC)_[F9915E0F].mkv
    re.compile(r'(\(?\[?){1}(?P<MediaInfo>AAC).*', re.IGNORECASE) 
]

MEDIA_INFO_ENCODING_REGEXS = [
    # h264, h265, x264
    re.compile(r'(\(?\[?){1}(?P<MediaInfo>(h|x)2\d{2}).*', re.IGNORECASE)  
]

MEDIA_INFO_COLOR_BITS_REGEXS = [
    # h264, h265, x264
    re.compile(r'(\(?\[?){1}(?P<MediaInfo>\d{1,2}\-bit).*', re.IGNORECASE)  
]

MEDIA_INFO_REGEXS = {
    'resolution': MEDIA_INFO_RESOLUTION_REGEXS,
    'source': MEDIA_INFO_SOURCE_REGEXS,
    'audio_source': MEDIA_INFO_AUDIO_SOURCE_REGEXS,
    'encoding': MEDIA_INFO_ENCODING_REGEXS,
    'color_bits': MEDIA_INFO_COLOR_BITS_REGEXS
}



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

def parse_anime_hash(filename):
    """ Given a filename, match hash and return hash with brackets. Returns None if no matches."""
    print_info('Extracting hash from {0}'.format(filename))
    for regex in ANIME_HASH_REGEXS:
        m = re.search(regex, filename)

        if m is None:
            continue

        ep_hash = m.group('Hash').upper()
        print_info('Extracted Hash: {0}'.format(ep_hash))
        return ep_hash
    
    return ''

def parse_anime_group(filename):
    """ Given a filename, match anime sub group and return group without brackets. Returns None if no matches."""
    print_info('Extracting hash from {0}'.format(filename))
    for regex in ANIME_GROUP_REGEXS:
        m = re.search(regex, filename)

        if m is None:
            continue

        ep_group = m.group('Group')
        print_info('Extracted Group: {0}'.format(ep_group))
        return ep_group
    
    return None

def parse_anime_episode(filename):
    """ Given a filename, matches episode and returns episode in E01 format. This will ignore episode parts. Returns None if no matches."""
    print_info('Extracting episode from {0}'.format(filename))
    for regex in ANIME_EPISODE_NUM_REGEXS:
        m = re.search(regex, filename)

        if m is None:
            continue

        extracted_ep = m.group('Episode')
        print_info('Extracted episode: {0}'.format(extracted_ep))

        ep_num = int(extracted_ep)
        if ep_num is not None and ep_num > 0:
            print_info('Episode might be: {0}'.format(ep_num))
            return 'E' + format_num(ep_num)

    return None

def parse_anime_episode_title(filename):
    """ Attempts to parse episode title from filename. Will strip out separators at start of string. If no title is found, returns empty string"""
    print_info('Attempting to parse episode title from {0}'.format(filename))
    for regex in ANIME_EPISODE_TITLE_REGEXS:
        m = re.search(regex, filename)

        if m is None:
            continue

        extracted_title = m.group('EpisodeTitle')
        return clean_episode_title(extracted_title)
    return ''

def parse_media_info(filename):
    """ Given a filename, match media info and return MediaInfo object. Returns empty MediaInfo if no matches."""
    print_info('Extracting hash from {0}'.format(filename))
    media_info = MediaInfo()
    for media_info_type in MEDIA_INFO_REGEXS:
        #print_info('Parsing for {0}'.format(media_info_type))
        for regex in MEDIA_INFO_REGEXS[media_info_type]:
            m = re.search(regex, filename)

            if m is None:
                continue

            extracted_data = m.group('MediaInfo').upper()
            print_info('Extracted {0}: {1}'.format(media_info_type, extracted_data))

            # Before we set, do any needed cleanup
            if media_info_type == 'resolution':
                if not extracted_data.endswith('p'):
                    resolution = int(extracted_data)
                    if resolution == 1280:
                        extracted_data = '720'
                    extracted_data = extracted_data + 'p'
                media_info.resolution = extracted_data
            if media_info_type == 'source':
                media_info.source = extracted_data.replace('-', '')
            elif media_info_type == 'audio_source':
                media_info.audio_source = extracted_data
            elif media_info_type == 'encoding':
                media_info.encoding = re.sub('X', 'H', extracted_data)
            elif media_info_type == 'color_bits':
                media_info.color_bits = extracted_data
            break
            
    
    return media_info

def clean_episode_title(filename):
    """ Removes special seperators like -,_  and leading spaces"""
    new_str = filename.replace('_', ' ').replace('-', ' ')
    return re.sub(r'\s+', ' ', new_str).strip()

def is_special_season(season_str):
    """ Returns True if Season is formated as Special (ie S00) """
    return season_str == 'S00'
    
def is_media_file(file):
    """ Returns true if file is a known media extension. This list is self-maintained. """
    return file.lower().endswith(MEDIA_EXTENSIONS)

def is_subtitle(file):
    """ Returns true if file is a known subtitle extension. This list is self-maintained. """
    return file.lower().endswith(SUBTITLE_EXTENSIONS)

def is_manga(file):
    """ Returns true if file is a known manga file extension. This list is self-maintained. """
    return file.lower().endswith(MANGA_EXTENSIONS)

def format_num(num):
    """ Formats a number to have leading 0 if below 10 """
    if num is None:
        return num
    if (num < 10):
        return '0' + str(num)
    return str(num)
 
if __name__ == '__main__':
    print('Hello')

