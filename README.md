# PyRenamer
This program is written to rename TV Series filenames to match what Plex or Sonarr needs to properly match. Often times many airings or downloads will not properly match the metadata ordering. This program remidies that by reading the filenames and remapping them into the standard format. This does it purely by Season and Episode numbers rather than attempting to match with a metadata provider.

# How to install
Download this from git and place somewhere on your computer. Put that location in PATH variable so you can execute from any directory.

# How to run
`python rename.py --show_name "My show here"`
This is the minimum required command to execute. You can get more commands from the rename.py file.

# BUGS:
Episode 21 - Mother And Child Reunion.avi -> Happy Days - S08E01 - Mother And Child Reunion.avi

# TODO:
* Implement Subtitle renaming and enhance to suport multiple subtitles per file (or handle normally) (test this)
* Implement seasons that are years. Ie S2003E01
* Implement season maps in conjunction with eps_per_file
