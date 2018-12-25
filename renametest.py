import unittest
import rename
import os
from episodeobj import EpisodeInfo
from episoderename import EpisodeRename

root_dir = os.path.abspath('./test-data/The Weekenders - Parts/')
weekenders_part_infos = []
info = EpisodeInfo(root_dir, 'S01E01a - Crush Test Dummies')
info.episode = 'E01'
info.extension = 'mp4'
info.part_num = 1
info.subtitle = None
info.title = 'Crush Test Dummies'
info.season = 'S01'
weekenders_part_infos.append(info)
info = EpisodeInfo(root_dir, 'S01E01b - Grow Up')
info.episode = 'E01'
info.extension = 'mp4'
info.part_num = 2
info.subtitle = None
info.title = 'Grow Up'
info.season = 'S01'
weekenders_part_infos.append(info)
info = EpisodeInfo(root_dir, 'S01E02a - Shoes of Destiny')
info.episode = 'E02'
info.extension = 'mp4'
info.part_num = 1
info.subtitle = None
info.season = 'S01'
info.title = 'Shoes of Destiny'
weekenders_part_infos.append(info)
info = EpisodeInfo(root_dir, 'S01E02b - Sense and Sensitivity')
info.episode = 'E02'
info.extension = 'mp4'
info.part_num = 2
info.subtitle = None
info.season = 'S01'
info.title = 'Sense and Sensitivity'
weekenders_part_infos.append(info)

#root_dir = os.path.abspath('./test-data/producing-parker - standard derived seasons/')
producing_parkers = []
info = EpisodeInfo(root_dir, 'producing-parker-season-1-episode-1-producing-parker')
info.episode = 'E01'
info.extension = 'mp4'
info.part_num = 0
info.subtitle = None
info.title = 'producingparker'
info.season = 'S01'
producing_parkers.append(info)
info = EpisodeInfo(root_dir, 'producing-parker-season-1-episode-2-producing-parker')
info.episode = 'E02'
info.extension = 'mp4'
info.part_num = 0
info.subtitle = None
info.title = 'producingparker'
info.season = 'S01'
producing_parkers.append(info)
info = EpisodeInfo(root_dir, 'producing-parker-season-2-episode-1-producing-parker')
info.episode = 'E01'
info.extension = 'mp4'
info.part_num = 0
info.subtitle = None
info.season = 'S02'
info.title = 'producingparker'
producing_parkers.append(info)

class Test_TestRename(unittest.TestCase):
    
    def test_generate_episode_infos(self):
        result = rename.generate_episode_infos(root_dir)
        """ for info in result:
            print(info) """
        self.assertListEqual(result, weekenders_part_infos)
    
    def test_generate_derived_season_renames(self):
        rename.show_name = 'Producing Parker'
        infos = rename.generate_episode_infos(os.path.abspath('./test-data/producing-parker - standard derived seasons/'))
        result = rename.generate_derived_season_renames(infos)
        print('results:')
        for r in result:
            print(r)
        correct_renames = []
        correct_renames.append(EpisodeRename('', 'Producing Parker - S01E01 - producingparker'))
        correct_renames.append(EpisodeRename('', 'Producing Parker - S01E02 - producingparker'))
        correct_renames.append(EpisodeRename('', 'Producing Parker - S02E01 - producingparker'))
        self.assertListEqual(result, correct_renames)
    
    def test_info_has_parts(self):
        self.assertTrue(rename.info_has_parts(weekenders_part_infos))
        self.assertFalse(rename.info_has_parts([]))
        self.assertFalse(rename.info_has_parts([EpisodeInfo(root_dir, 'S01E02b - Sense and Sensitivity')]))
        
    
if __name__ == '__main__':
    unittest.main()
