import unittest
import rename
import os
from episodeobj import EpisodeInfo
from episoderename import EpisodeRename
import generate_test_data as TestDataGenerator

root_dir = os.path.abspath('./tests/cases/The Weekenders - Parts/')
weekenders_part_infos = []
info = EpisodeInfo(root_dir, 'S01E01a - Crush Test Dummies.mp4')
info.episode = 'E01'
info.extension = 'mp4'
info.part_num = 1
info.subtitle = None
info.title = 'Crush Test Dummies'
info.season = 'S01'
weekenders_part_infos.append(info)
info = EpisodeInfo(root_dir, 'S01E01b - Grow Up.mp4')
info.episode = 'E01'
info.extension = 'mp4'
info.part_num = 2
info.subtitle = None
info.title = 'Grow Up'
info.season = 'S01'
weekenders_part_infos.append(info)
info = EpisodeInfo(root_dir, 'S01E02a - Shoes of Destiny.mp4')
info.episode = 'E02'
info.extension = 'mp4'
info.part_num = 1
info.subtitle = None
info.season = 'S01'
info.title = 'Shoes of Destiny'
weekenders_part_infos.append(info)
info = EpisodeInfo(root_dir, 'S01E02b - Sense and Sensitivity.mp4')
info.episode = 'E02'
info.extension = 'mp4'
info.part_num = 2
info.subtitle = None
info.season = 'S01'
info.title = 'Sense and Sensitivity'
weekenders_part_infos.append(info)
info = EpisodeInfo(root_dir, 'S01E03a - Shoes.mp4')
info.episode = 'E03'
info.extension = 'mp4'
info.part_num = 1
info.subtitle = None
info.season = 'S01'
info.title = 'Shoes'
weekenders_part_infos.append(info)

# TODO: Validate the rootpath here
producing_parkers = []
info = EpisodeInfo(root_dir, 'producing-parker-season-1-episode-1-producing-parker')
info.episode = 'E01'
info.extension = 'mp4'
info.part_num = 0
info.subtitle = None
info.title = 'producing parker'
info.season = 'S01'
producing_parkers.append(info)
info = EpisodeInfo(root_dir, 'producing-parker-season-1-episode-2-producing-parker')
info.episode = 'E02'
info.extension = 'mp4'
info.part_num = 0
info.subtitle = None
info.title = 'producing parker'
info.season = 'S01'
producing_parkers.append(info)
info = EpisodeInfo(root_dir, 'producing-parker-season-2-episode-1-producing-parker')
info.episode = 'E01'
info.extension = 'mp4'
info.part_num = 0
info.subtitle = None
info.season = 'S02'
info.title = 'producing parker'
producing_parkers.append(info)



    


class Test_TestRename(unittest.TestCase):

    maxDiff = None

    @classmethod
    def setUpClass(self):
        '''Unpack tests/ directory. Any -tests.txt files should be expanded into fake .mp4 files'''
        for _, _, files in os.walk(os.path.abspath('./tests/cases/')):
            for file in files:
                if file.endswith('-testcase.txt'):
                    filepath = os.path.join(os.path.abspath('./tests/cases/'), file)
                    TestDataGenerator.generate_data(filepath, os.path.abspath('./tests/cases/'))
    
    @classmethod
    def tearDownClass(self):
        ''' Delete everything inside the tests/cases/ directory'''
        TestDataGenerator.clean_up_generated_data(os.path.abspath('./tests/cases/'))

    
    
    def test_generate_episode_infos(self):
        root_dir = os.path.abspath('./tests/cases/The Weekenders - Parts/')
        result = rename.generate_episode_infos(root_dir)
        self.assertListEqual(result, weekenders_part_infos)
    
    def test_generate_part_renames(self):
        rename.show_name = 'The Weekenders'
        result = rename.generate_part_renames(weekenders_part_infos)

        correct_renames = []
        correct_renames.append(EpisodeRename('S01E01a - Crush Test Dummies.mp4', 'The Weekenders - S01E01 - Crush Test Dummies.mp4'))
        correct_renames.append(EpisodeRename('S01E01b - Grow Up.mp4', 'The Weekenders - S01E02 - Grow Up.mp4'))
        correct_renames.append(EpisodeRename('S01E02a - Shoes of Destiny.mp4', 'The Weekenders - S01E03 - Shoes of Destiny.mp4'))
        correct_renames.append(EpisodeRename('S01E02b - Sense and Sensitivity.mp4', 'The Weekenders - S01E04 - Sense and Sensitivity.mp4'))
        correct_renames.append(EpisodeRename('S01E03a - Shoes.mp4', 'The Weekenders - S01E05 - Shoes.mp4'))
        self.assertListEqual(result, correct_renames)
    
    def test_generate_multiple_part_per_file_renames(self):
        rename.show_name = 'Producing Parker'
        rename.eps_per_file = 2
        infos = rename.generate_episode_infos(os.path.abspath('./tests/cases/Producing Parker/'))
        result = rename.generate_multiple_part_per_file_renames(infos)

        correct_renames = []
        correct_renames.append(EpisodeRename('producing-parker-season-1-episode-1-producing-parker.mp4', 'Producing Parker - S01E01-E02 - producing parker.mp4'))
        correct_renames.append(EpisodeRename('producing-parker-season-1-episode-2-producing-parker.mp4', 'Producing Parker - S01E03-E04 - producing parker.mp4'))
        correct_renames.append(EpisodeRename('producing-parker-season-2-episode-1-producing-parker.mp4', 'Producing Parker - S02E01-E02 - producing parker.mp4'))
        self.assertListEqual(result, correct_renames)

    
    def test_generate_derived_season_renames(self):
        rename.show_name = 'Producing Parker'
        infos = rename.generate_episode_infos(os.path.abspath('./tests/cases/Producing Parker/'))
        result = rename.generate_derived_season_renames(infos)

        correct_renames = []
        correct_renames.append(EpisodeRename('producing-parker-season-1-episode-1-producing-parker.mp4', 'Producing Parker - S01E01 - producing parker.mp4'))
        correct_renames.append(EpisodeRename('producing-parker-season-1-episode-2-producing-parker.mp4', 'Producing Parker - S01E02 - producing parker.mp4'))
        correct_renames.append(EpisodeRename('producing-parker-season-2-episode-1-producing-parker.mp4', 'Producing Parker - S02E01 - producing parker.mp4'))
        self.assertListEqual(result, correct_renames)

    def test_generate_derived_season_renames_2(self):
        rename.show_name = 'Producing Parker'
        infos = []
        info = EpisodeInfo(root_dir, 'producing-parker-season-2-episode-6-15-minutes-in-parker.mp4')
        info.episode = 'E06'
        info.extension = 'mp4'
        info.part_num = 0
        info.subtitle = None
        info.season = 'S02'
        info.title = '15 minutes in parker'
        infos.append(info)
        result = rename.generate_derived_season_renames(infos)

        self.assertListEqual(result, [EpisodeRename('producing-parker-season-2-episode-6-15-minutes-in-parker.mp4', 'Producing Parker - S02E06 - 15 minutes in parker.mp4')])
    
    def test_generate_derived_season_renames_3(self):
        rename.show_name = 'Martin Mystery'
        infos = []
        # For this test, assume Episode 65, even though this was for a season_maps exercise
        info = EpisodeInfo(root_dir, 'martin-mystery-episode-65-its-alive-part-1.mp4')
        info.episode = 'E65'
        info.extension = 'mp4'
        info.part_num = 0
        info.subtitle = None
        info.season = 'S01'
        info.title = 'its alive part 1'
        infos.append(info)
        result = rename.generate_derived_season_renames(infos)

        self.assertListEqual(result, [EpisodeRename('martin-mystery-episode-65-its-alive-part-1.mp4', 'Martin Mystery - S01E65 - its alive part 1.mp4')])
    
    def test_generate_season_map_file_renames(self):
        rename.show_name = 'Producing Parker'
        rename.season_maps = [1, 2]
        infos = rename.generate_episode_infos(os.path.abspath('./tests/cases/Producing Parker - season maps/'))
        result = rename.generate_season_map_file_renames(infos)

        correct_renames = []
        correct_renames.append(EpisodeRename('producing-parker-season-1-episode-1-producing-parker.mp4', 'Producing Parker - S01E01 - producing parker.mp4'))
        correct_renames.append(EpisodeRename('producing-parker-season-1-episode-2-producing-parker.mp4', 'Producing Parker - S02E01 - producing parker.mp4'))
        correct_renames.append(EpisodeRename('producing-parker-season-1-episode-3-producing-parker.mp4', 'Producing Parker - S02E02 - producing parker.mp4'))
        
        self.assertListEqual(result, correct_renames)

    def test_generate_season_map_file_renames_for_anime_1(self):
        rename.show_name = 'Gurren Lagann'
        rename.season_maps = [1, 2]
        infos = rename.generate_episode_infos(os.path.abspath('./tests/cases/Anime Season Maps/'))
        result = rename.generate_season_map_file_renames(infos)

        correct_renames = []
        correct_renames.append(EpisodeRename('[CBM]_Gurren_Lagann_-_01_-_Bust_Through_the_Heavens_With_Your_Drill!_[720p]_[D2E69407].mkv', '[CBM] Gurren Lagann - S01E01 - Bust Through the Heavens With Your Drill! [720p] [D2E69407].mp4'))
        correct_renames.append(EpisodeRename('[CBM]_Gurren_Lagann_-_02_-_I_Said_I\'m_Gonna_Pilot_That_Thing!!_[720p]_[19E9CF6F].mkv', 'Producing Parker - S02E01 - producing parker.mp4'))
        correct_renames.append(EpisodeRename('[CBM]_Gurren_Lagann_-_03_-_Who_Do_You_Think_You_Are,_Having_Two_Faces!_[720p]_[659E4875].mkv', 'Producing Parker - S02E02 - producing parker.mp4'))
        
        self.assertListEqual(result, correct_renames)
    
    def test_info_has_parts(self):
        self.assertTrue(rename.info_has_parts(weekenders_part_infos))
        self.assertFalse(rename.info_has_parts([]))
        self.assertFalse(rename.info_has_parts([EpisodeInfo(root_dir, 'S01E02b - Sense and Sensitivity')]))
    
    def test_sum_until(self):
        self.assertIs(rename.sum_until([1, 1, 1, 2], 1), 1)
        self.assertIs(rename.sum_until([1, 1, 1, 2], 0), 0)
        
    
if __name__ == '__main__':
    unittest.main()
