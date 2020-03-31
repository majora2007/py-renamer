class EpisodeInfo(object):
    episode = None
    season = None
    part_num = None
    root_dir = None
    original_filename = None
    extension = ''
    subtitle = None
    title = '' # Rest of the filename outside of show, season, episode

    def __init__(self, root_dir, filename):
        self.root_dir = root_dir
        self.original_filename = filename
    
    def __eq__(self, other):
        return self.episode == other.episode and self.season == other.season and self.part_num == other.part_num and self.root_dir == other.root_dir and self.original_filename == other.original_filename and self.extension == other.extension and self.subtitle == other.subtitle and self.title == other.title
    
    def __str__(self):
        return 'File: {0}\n\tRoot Dir: {1}\n\tExtension: {2}\n\tSubtitle: {3}\n\tEpisode Num: {4}\n\tSeason: {5}\n\tPart Num: {6}\n\tTitle: {7}\n\n'.format(self.original_filename, self.root_dir, self.extension, self.subtitle, self.episode, self.season, self.part_num, self.title)