class EpisodeInfo(object):
    episode = None
    season = None
    part_num = 0
    root_dir = None
    original_filename = None
    extension = ''
    subtitle = None
    title = '' # Rest of the filename outside of show, season, episode
    media_info = '' # Info like 720p, source, audio channels, etc

    hash_code = '' # Used in anime parsing
    scene_group = '' # Used in anime parsing

    def __init__(self, root_dir, filename):
        self.root_dir = root_dir
        self.original_filename = filename
    
    def __eq__(self, other):
        return self.episode == other.episode and self.season == other.season and self.part_num == other.part_num and self.root_dir == other.root_dir and self.original_filename == other.original_filename and self.extension == other.extension and self.subtitle == other.subtitle and self.title == other.title and self.hash_code == other.hash_code and self.scene_group == other.scene_group
    
    def __str__(self):
        return 'File: {0}\n\tRoot Dir: {1}\n\tExtension: {2}\n\tSubtitle: {3}\n\tEpisode Num: {4}\n\tSeason: {5}\n\tPart Num: {6}\n\tTitle: {7}\n\tHash: {8}\n\tGroup: {9}\n\n'.format(self.original_filename, self.root_dir, self.extension, self.subtitle, self.episode, self.season, self.part_num, self.title, self.hash_code, self.scene_group)
    
    def __repr__(self):
        return 'File: {0}\n\tRoot Dir: {1}\n\tExtension: {2}\n\tSubtitle: {3}\n\tEpisode Num: {4}\n\tSeason: {5}\n\tPart Num: {6}\n\tTitle: {7}\n\tHash: {8}\n\tGroup: {9}\n\n'.format(self.original_filename, self.root_dir, self.extension, self.subtitle, self.episode, self.season, self.part_num, self.title, self.hash_code, self.scene_group)