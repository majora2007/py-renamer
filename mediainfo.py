class MediaInfo(object):
    resolution = '' # 720p, 1080p
    source = '' # BD, WEBRip
    audio_source = '' # FLAC
    color_bits = '8' # 10-bit color
    encoding = 'H264'

    def __init__(self, resolution='', source='', audio_source='', color_bits='8', encoding='H264'):
        self.resolution = resolution
        self.source = source
        self.audio_source = audio_source
        self.color_bits = color_bits
        self.encoding = encoding
    
    def __str__(self):
        return 'MediaInfo: \n\tResolution: {0}\n\tSource: {1}\n\tAudio Source: {2}\n\tColor Bits: {3}\n\tEncoding: {4}\n\n'.format(self.resolution, self.source, self.audio_source, self.color_bits, self.encoding)
    
    def __repr__(self):
        return 'MediaInfo: \n\tResolution: {0}\n\tSource: {1}\n\tAudio Source: {2}\n\tColor Bits: {3}\n\tEncoding: {4}\n\n'.format(self.resolution, self.source, self.audio_source, self.color_bits, self.encoding)

    def __eq__(self, other):
        return self.resolution == other.resolution and self.source == other.source and self.audio_source == other.audio_source and self.color_bits == other.color_bits and self.encoding == other.encoding