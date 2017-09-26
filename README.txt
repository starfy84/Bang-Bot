Stuff Complete:
	- Commands: help, start, join, leave, players
    - Game queuing behaviours
    - Player initialization when Game begins
    	- Characters, Roles, Placement on Map
    
Non-Priority Goals:
	- Better aesthetics for help command info
    - Better aesthetics for players command
    
Immediate Issues:
    - start command
	- We need the round system to be implemented
    	- Keep track of gamestate, know what to expect from players
	- The deck and dealing cards
    	- Player hand commands (hand, draw, discard, play)
        
================================================================================================================================================
ARCHIVE OF CHANGES

2017-09-22 10:26PM (Queue Test [game.py, player.py, text.py, main.py])
- Identified and fixed bugs in all commands
	- help, start, join, leave, players are all stable
- Queuing works
- Tested with multiple people
- Identified issue with help - looks nasty with embeds

2017-09-24 8:43PM (Offline Test [game.py, player.py, text.py])
- Identified and fixed bug in game.setup
- Changed keys in map_presets[capacity] to "Players" from "Players:"
	- 9 is now default value for empty tile (0-3 are for roles)
    - Fixed errors in map_presets (characters overlapped)
- Fixed difference in character names in game.py and text.py
- Roles stored as int in player (0-3), must be checked as such
	- Refers to index of list text.roles containing roles
    
2017-09-25 8:57PM (Minor Update and Check [game.py, player.py])
- Tested all map presets for player capacities from 4 to 8
- Added __str__ method for game.py
- Removed player.draw_card(), added game.deal_card()