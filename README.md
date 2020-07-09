# PyRenamer
This program is written to rename TV Series filenames to match what Plex or Sonarr needs to properly match. Often times many airings or downloads will not properly match the metadata ordering. This program remidies that by reading the filenames and remapping them into the standard format. This does it purely by Season and Episode numbers rather than attempting to match with a metadata provider.

# How to install
Download this from git and place somewhere on your computer. Put that location in PATH variable so you can execute from any directory.

# How to run
`python rename.py --show_name "My show here"`
This is the minimum required command to execute. You can get more commands from the rename.py file.

# Arguments
|   Argument Name	|   Required	|   Description	|   Argument Type	|   Notes	|
|---	            |---	        |---	        |---	        |---	    |
|   show_name  	    |   ✓	        |   	The name of the show. This does not perform parsing, just blinding pastes it. Can be used to transfer quality info if not in the filename.        |   	 String       |   	    |
|   season	        |   x	        |   	Forces the season, will ignore what the parser says        |   	   Number     |   	    |
|   eps_per_file	|   x	        |   	If a file has multiple episodes, this will generate multiple episodes per file.         |   	  Number      |   	Show - ep1a - ep1b -> Show - S01E01-E02    |
|   dry	|   x	        |   	Used to preview the changes without modifying files on disk         |   	  None      |   	Just supply the flag    |
|   verbose	|   x	        |   	Print debug information         |   	  None      |   	Just supply the flag    |
|   season_maps	|   x	        |   	Maps ordered episodes into Seasons. Useful for absolute to seasons         |   	  Array of Numbers      |   	ie) [1, 2]. First episode goes to Season 1, next 2 episodes goes to Season 2    |
|   anime	|   x	        |   	Use anime parsing and renaming rules. Will generate Media Info and Hash and keep scene group         |   	  None      |   	Does not work with eps_per_file    |
|   offset	|   x	        |   	If passed, episodes will start at the offset         |   	  Number      |   	ie) episode 1 with offset of 4 writes as episode 5. Useful for combining seasons together. Does not work with season maps.    |

