# PyRenamer
This program is written to rename TV Series filenames to match what Plex or Sonarr needs to properly match. Often times many airings or downloads will not properly match the metadata ordering. This program remidies that by reading the filenames and remapping them into the standard format. This does it purely by Season and Episode numbers rather than attempting to match with a metadata provider.

# How to install
Download this from git and place somewhere on your computer. Put that location in PATH variable so you can execute from any directory.

# How to run
`python rename.py --show_name "My show here"`
This is the minimum required command to execute. You can get more commands from the rename.py file.

# BUGS:
producing-parker-season-2-episode-11-3.0-parker.mp4 mapped to producing parker s03e06 - .mp4
producing-parker-season-2-episode-6-15-minutes-in-parker.mp4 mapped to producing parker s02E15 - minutes in parker.mp4
Happy_Days_-_3-21_-_Fonzie_Moves_In_-_DVD2XviD -> Happy Days - S03E01 - Fonzie Moves In DVD2XviD
Braceface - 201 - The Social Fabric part 1.mkv -> Braceface - S01E201 - .mkv
TMNT - S05E21 - Planet Of The Turtleoids Part 1.mp4 -> Teenage Mutant Ninja Turtles - S05E21 - .mp4

# TODO:
* Implement Subtitle renaming and enhance to suport multiple subtitles per file (or handle normally)
* Enhance parser to support more formats
* Implement ability to pass in a set of episode counts that map abs numbers to seasons (ie: [2, 2, 3] => 2 eps in S01, 2 eps in S02, 3 eps in S03)
