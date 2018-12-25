class EpisodeRename(object):
    original_filename = ''
    new_filename = ''

    def __init__(self, original_filename, new_filename):
        self.original_filename = original_filename
        self.new_filename = new_filename
    
    def __str__(self):
        return '{0} -> {1}'.format(self.original_filename, self.new_filename)

    def __eq__(self, other):
        return self.new_filename == other.new_filename