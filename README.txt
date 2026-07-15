================================
        PAC-MAN
================================

HOW TO RUN
----------
Simply double-click the 'pac-man' executable, or run it from the terminal:
    ./pac-man

CONTROLS
--------
Movement:   W / A / S / D
Pause:      ESC

CHEAT MODE (for evaluation purposes)
-------------------------------------
I   - Toggle Invincibility (ghosts cannot eat you)
F   - Toggle Freeze Ghosts (ghosts stop moving)
L   - Skip to next level
B   - Go back to previous level
M   - Add an extra life

Note: Scores achieved with cheats enabled are NOT saved to the highscore list.

CONFIGURATION
-------------
The game configuration is loaded from 'config/config.json'.
You can modify the following values:

    highscore_filename      - Path to the highscore file (default: highscores.json)
    lives                   - Number of starting lives (default: 3)
    seed                    - Maze seed for level 1 (default: 42)
    level_max_time          - Time limit per level in seconds (default: 90)
    pacgum                  - Number of pacgums per level (default: 10)
    points_per_pacgum       - Points per pacgum eaten (default: 10)
    points_per_super_pacgum - Points per super-pacgum eaten (default: 50)
    points_per_ghost        - Points per ghost eaten (default: 200)
    ghost_respawn_time      - Seconds for ghost to respawn after being eaten (default: 5.0)
    ghost_flee_time         - Seconds ghosts stay edible after a super-pacgum (default: 7.0)
    levels                  - List of maze sizes [(width, height), ...]

Comments starting with # are supported in the config file.

HIGHSCORES
----------
The top 10 highscores are saved automatically at the end of each game.
Scores are stored in 'highscores.json'.

================================
Created as part of the 42 curriculum
================================
