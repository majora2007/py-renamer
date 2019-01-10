# PyRenamer
This program is written to rename TV Series filenames to match what Plex or Sonarr needs to properly match. Often times many airings or downloads will not properly match the metadata ordering. This program remidies that by reading the filenames and remapping them into the standard format. This does it purely by Season and Episode numbers rather than attempting to match with a metadata provider.

# How to install
Download this from git and place somewhere on your computer. Put that location in PATH variable so you can execute from any directory.

# How to run
`python rename.py --show_name "My show here"`
This is the minimum required command to execute. You can get more commands from the rename.py file.

# BUGS:


# TODO:
* Implement Subtitle renaming and enhance to suport multiple subtitles per file (or handle normally) (test this)
* Implement ability to pass in a set of episode counts that map abs numbers to seasons (ie: [2, 2, 3] => 2 eps in S01, 2 eps in S02, 3 eps in S03)
