import unittest
import parse
from mediainfo import MediaInfo

class Test_TestParse(unittest.TestCase):
    def test_parse_season(self):
        self.assertEqual(parse.parse_season('101'), 'S01')
        self.assertEqual(parse.parse_season('2x01'), 'S02')
        self.assertEqual(parse.parse_season('S01E02'), 'S01')
        self.assertEqual(parse.parse_season('2x01'), 'S02')
        self.assertEqual(parse.parse_season('Happy Days 11-01 '), 'S11')
        self.assertEqual(parse.parse_season('S01E02a - Shoes of Destiny'), 'S01')
        self.assertEqual(parse.parse_season('producing-parker-season-2-episode-1-producing-parker'), 'S02')
        self.assertEqual(parse.parse_season('Happy_Days_-_3-21_-_Fonzie_Moves_In_-_DVD2XviD'), 'S03')
        self.assertEqual(parse.parse_season('Braceface - 201 - The Social Fabric part 1.mkv'), 'S02')
        self.assertEqual(parse.parse_season('Martin Mystery 201'), 'S02')
        self.assertEqual(parse.parse_season('producing-parker-season-2-episode-11-3.0-parker.mp4'), 'S02')
        self.assertEqual(parse.parse_season('sabrinas-secret-life-2003-episode-1-at-the-hop'), 'S2003')
        self.assertEqual(parse.parse_season('s1ep01 the girls want to go to a nightclub.avi'), 'S01')
        self.assertEqual(parse.parse_season('s1ep35 ricky asks for a raise.avi'), 'S01')
        
        
    
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
        self.assertEqual(parse.parse_episode('Happy_Days_-_3-21_-_Fonzie_Moves_In_-_DVD2XviD'), 'E21')
        self.assertEqual(parse.parse_episode('Braceface - 201 - The Social Fabric part 1.mkv'), 'E01')
        self.assertEqual(parse.parse_episode('Martin Mystery 201'), 'E01')
        self.assertEqual(parse.parse_episode('martin mystery 325 its alive part 1 [tv.dtv.mere].avi'), 'E25')
        self.assertEqual(parse.parse_episode('producing-parker-season-2-episode-11-3.0-parker.mp4'), 'E11')
        self.assertEqual(parse.parse_episode('martin-mystery-episode-65-its-alive-part-1'), 'E65')
        self.assertEqual(parse.parse_episode('sabrinas-secret-life-2003-episode-1-at-the-hop'), 'E01')
        self.assertEqual(parse.parse_episode('Episode 21 - Mother And Child Reunion.avi'), 'E21')
        self.assertEqual(parse.parse_episode('Happy Days 11-22 Fonzies Spots.avi'), 'E22')
        self.assertEqual(parse.parse_episode('YP-WOY-01x38-1R-The_Rider.mkv'), 'E38')
        self.assertEqual(parse.parse_episode('s1ep02 be a pal.avi'), 'E02')

        
    def test_parse_anime_hash(self):
        self.assertEqual(parse.parse_anime_hash('[Coalgirls]_Ro-Kyu-Bu!_SS_01_(1280x720_Blu-Ray_FLAC)_[E1AC4C4A].mkv'), '[E1AC4C4A]')    
        self.assertEqual(parse.parse_anime_hash('[Doki]_30-sai_no_Hoken_Taiiku_-_01v2_(1280x720_h264_BD_AAC)_[F9915E0F].mkv'), '[F9915E0F]')
        self.assertEqual(parse.parse_anime_hash('[Judas] Masamune-kun no Revenge - 01.mkv'), '')
        
    def test_parse_anime_group(self):
        self.assertEqual(parse.parse_anime_group('[Coalgirls]_Ro-Kyu-Bu!_SS_01_(1280x720_Blu-Ray_FLAC)_[E1AC4C4A].mkv'), 'Coalgirls')    
        self.assertEqual(parse.parse_anime_group('[Doki]_30-sai_no_Hoken_Taiiku_-_01v2_(1280x720_h264_BD_AAC)_[F9915E0F].mkv'), 'Doki')
    
    def test_parse_anime_episode(self):
        self.assertEqual(parse.parse_anime_episode('[Coalgirls]_Ro-Kyu-Bu!_SS_01_(1280x720_Blu-Ray_FLAC)_[E1AC4C4A].mkv'), 'E01')    
        self.assertEqual(parse.parse_anime_episode('[Doki]_30-sai_no_Hoken_Taiiku_-_01v2_(1280x720_h264_BD_AAC)_[F9915E0F].mkv'), 'E01')
        self.assertEqual(parse.parse_anime_episode('[Judas] Masamune-kun no Revenge - 01.mkv'), 'E01')
        self.assertEqual(parse.parse_anime_episode('(Hi10)Hajime_no_Ippo_New_Challenger-25(720p)(SZN&_IO).mkv'), 'E25')

    def test_parse_anime_episode_title(self):
        self.assertEqual(parse.parse_anime_episode_title('[Coalgirls]_Ro-Kyu-Bu!_SS_01_(1280x720_Blu-Ray_FLAC)_[E1AC4C4A].mkv'), '')    
        self.assertEqual(parse.parse_anime_episode_title('[Doki]_30-sai_no_Hoken_Taiiku_-_01v2_(1280x720_h264_BD_AAC)_[F9915E0F].mkv'), '')
        self.assertEqual(parse.parse_anime_episode_title('[CBM]_Gurren_Lagann_-_01_-_Bust_Through_the_Heavens_With_Your_Drill!_[720p]_[D2E69407].mkv'), 'Bust Through the Heavens With Your Drill!')
        self.assertEqual(parse.parse_anime_episode_title('[CBM]_Gurren_Lagann_-_02_-_I_Said_I\'m_Gonna_Pilot_That_Thing!!_[720p]_[19E9CF6F].mkv'), 'I Said I\'m Gonna Pilot That Thing!!')
        

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
        #self.assertEqual(parse.parse_episode_part('s1ep02 be a pal.avi'), 0)
    
    def test_parse_episode_title(self):
        self.assertEqual(parse.parse_episode_title('S01E02'), '')
        self.assertEqual(parse.parse_episode_title('Grojband-episode 1a'), '')
        self.assertEqual(parse.parse_episode_title('S01E02a-title'), 'title')
        self.assertEqual(parse.parse_episode_title('Show name - S01E01 - Title here'), 'Title here')
        self.assertEqual(parse.parse_episode_title('[hash]_show_1x01_-_title_goes_here'), 'title goes here')
        self.assertEqual(parse.parse_episode_title('TMNT - S05E21 - Planet Of The Turtleoids Part 1'), 'Planet Of The Turtleoids Part 1')
        self.assertEqual(parse.parse_episode_title('martin-mystery-episode-65-its-alive-part-1'), 'its alive part 1')
        self.assertEqual(parse.parse_episode_title('Happy_Days_-_3-24_-_Arnold_s_Wedding_-_DVD2XviD'), 'Arnold s Wedding DVD2XviD')
        self.assertEqual(parse.parse_episode_title('Happy Days 11-01 Because It\'s There'), 'Because It\'s There')
        self.assertEqual(parse.parse_episode_title('larva-season-2-episode-34-one-wild-rough-tough-world-2-3'), 'one wild rough tough world 2 3')
        self.assertEqual(parse.parse_episode_title('s1ep02 be a pal'), 'be a pal')
        self.assertEqual(parse.parse_episode_title('BBC.Natures.Microworlds.01of13.Galapagos.720p.HDTV.x264.AAC.MVGroup.org'), '.Galapagos.720p.HDTV.x264.AAC.MVGroup.org')


    def test_parse_volume(self):
        self.assertEqual(parse.parse_volume('101'), 'Volume 0')

        

    def test_parse_media_info(self):
        self.assertEqual(parse.parse_media_info('[Coalgirls]_Ro-Kyu-Bu!_SS_01_(1280x720_Blu-Ray_FLAC)_[E1AC4C4A].mkv'), MediaInfo('720p', 'BLURAY', 'FLAC', '8', ''))
        self.assertEqual(parse.parse_media_info('[Doki]_30-sai_no_Hoken_Taiiku_-_01v2_(1280x720_h264_BD_AAC)_[F9915E0F].mkv'), MediaInfo('720p', 'BD', 'AAC', '8', 'H264'))
        self.assertEqual(parse.parse_media_info('[UTW]_Accel_World_-_01_[h264-720p][7A2BE7A5].mkv'), MediaInfo('720p', '', '', '8', 'H264'))
        self.assertEqual(parse.parse_media_info('Brooklyn.Nine-Nine.S07E07.720p.HDTV.x264-KILLERS'), MediaInfo('720p', 'HDTV', '', '8', 'H264'))

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
