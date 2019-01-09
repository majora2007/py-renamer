import unittest
import parse

class Test_TestParse(unittest.TestCase):
    def test_parse_season(self):
        self.assertEqual(parse.parse_season('101'), 'S01')
        self.assertEqual(parse.parse_season('2x01'), 'S02')
        self.assertEqual(parse.parse_season('S01E02'), 'S01')
        self.assertEqual(parse.parse_season('2x01'), 'S02')
        self.assertEqual(parse.parse_season('Happy Days 11-01 '), 'S11')
        self.assertEqual(parse.parse_season('S01E02a - Shoes of Destiny'), 'S01')
        self.assertEqual(parse.parse_season('producing-parker-season-2-episode-1-producing-parker'), 'S02')
        #self.assertEqual(parse.parse_season('Happy_Days_-_3-21_-_Fonzie_Moves_In_-_DVD2XviD'), 'S03')
        #self.assertEqual(parse.parse_season('Braceface - 201 - The Social Fabric part 1.mkv'), 'S02')
        self.assertEqual(parse.parse_season('Martin Mystery 201'), 'S02')
        
    
    def test_parse_episode(self):
        self.assertEqual(parse.parse_episode('S02E01'), 'E01')
        self.assertEqual(parse.parse_episode('S02E01A'), 'E01')
        self.assertEqual(parse.parse_episode('2x01'), 'E01')
        self.assertEqual(parse.parse_episode('Ep1'), 'E01')
        self.assertEqual(parse.parse_episode('Episode 1'), 'E01')
        self.assertEqual(parse.parse_episode('S04E01-E02'), 'E01-E02')
        self.assertEqual(parse.parse_episode('S04E01-E04'), 'E01-E04')
        self.assertEqual(parse.parse_episode('Grojband - some title'), None)
        self.assertEqual(parse.parse_episode('Happy Days 11-01'), 'E01')
        self.assertEqual(parse.parse_episode('producing-parker-season-2-episode-1-producing-parker'), 'E01')
        #self.assertEqual(parse.parse_episode('Happy_Days_-_3-21_-_Fonzie_Moves_In_-_DVD2XviD'), 'E21')
        #self.assertEqual(parse.parse_episode('Braceface - 201 - The Social Fabric part 1.mkv'), 'E01')
        self.assertEqual(parse.parse_episode('Martin Mystery 201'), 'E01')
        self.assertEqual(parse.parse_episode('martin mystery 325 its alive part 1 [tv.dtv.mere].avi'), 'E25')
    
    def test_parse_episode_part(self):
        self.assertEqual(parse.parse_episode_part('S01E02'), 0)
        self.assertEqual(parse.parse_episode_part('Grojband - S01E01A'), 1)
        self.assertEqual(parse.parse_episode_part('2x01C'), 3)
        self.assertEqual(parse.parse_episode_part('S01E02B'), 2)
        self.assertEqual(parse.parse_episode_part('Ep1a'), 1)
        self.assertEqual(parse.parse_episode_part('Ep1'), 0)
        self.assertEqual(parse.parse_episode_part('Show - 1a'), 1)
        self.assertEqual(parse.parse_episode_part('Show - 1'), 0)
        self.assertEqual(parse.parse_episode_part('Grojband - S01E01'), 0)
    
    def test_parse_episode_title(self):
        self.assertEqual(parse.parse_episode_title('S01E02'), '')
        self.assertEqual(parse.parse_episode_title('Grojband-episode 1a'), '')
        self.assertEqual(parse.parse_episode_title('S01E02a-title'), 'title')
        self.assertEqual(parse.parse_episode_title('Show name - S01E01 - Title here'), 'Title here')
        self.assertEqual(parse.parse_episode_title('[hash]_show_1x01_-_title_goes_here'), 'title goes here')

    def test_is_media_file(self):
        self.assertEqual(parse.is_media_file('joe.mp4'), True)
        self.assertEqual(parse.is_media_file('joe.mp3'), False)
        self.assertEqual(parse.is_media_file('joe.avi'), True)
        self.assertEqual(parse.is_media_file('joe.mkv'), True)
        self.assertEqual(parse.is_media_file('joe.str'), False)

    def test_format_num(self):
        self.assertEqual(parse.format_num(1), '01')
        self.assertEqual(parse.format_num(11), '11')
        self.assertEqual(parse.format_num(None), None)
    
    def test_is_special_season(self):
        self.assertEqual(parse.is_special_season('S01'), False)
        self.assertEqual(parse.is_special_season('S00'), True)
    
    def test_clean_episode_title(self):
        self.assertEqual(parse.clean_episode_title('- title'), 'title')
        self.assertEqual(parse.clean_episode_title('_-_title'), 'title')

if __name__ == '__main__':
    unittest.main()
