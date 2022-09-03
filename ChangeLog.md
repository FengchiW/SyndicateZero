========================
|    Syndicate Zero    |
========================

# Change Log

Changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
Post Version 1.1.5, this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2022-08-16
  ### General
    - Project started
    - Worked on the basic outline of the code
    - Added Raylib and setup the underlying game engine
    - Worked on conceptualizing the game

## [1.01.00] - 2022-08-17
  ### General
    - Added the game loop
    - Finished the conceptualizing of the game
    - Began working on the actual game mechanics
    - Generated art for the game

## [1.02.00] - 2022-08-18
  ### General
    - Started laying out the other scenes and the game mechanics
    - Continued working on the main game starting with a single level

## [1.03.00] - 2022-08-19
  ### General
    - Last update before vacation
    - Going to make small progress with some basic game setup
    - Reworking some of the file structure
    - Investigate the best method to save game data
    - Adding to github repository
    - First commit documented in github
    - Added a hover effect to the tiles in the game [needs reworking]

## [1.04.22828X] - 2022-08-22
  ### General
    - Updated how the rectangular grid is drawn, now the rectangles are inside the map object
    - Updated how tile hover is handled [in map obj]
    - Changed map obj to a tuple instead of a pair
    - Fixed the header guards on some files
    - Created a Tile Class and moved it into its own file
    - Fixed issues with the games hover detection
    - Renamed the python partner program to packager
    - Resolved some name conflict issues
    - Removed the last hovered tile from game class as its now unneeded
    - Removed all the padding stuff I don't like how its done reworking
    - Added an alpha layer for hover effects
    - Changed the way numbers work now MAJOR.MINOR[PUSH].YYMDD

## [1.1.5] - 2022-08-29
  ### General
    - I don't like the versioning structure so I changed it again
    - New versions will be Major.Minor.[CommitNo]
    - Major will have large titles
    - Minors will also have small titles
    - Majors updates every release
    - Minors updates every beta [large commit] and reset every release
    - Working on quick splash screen and possibly the main menu
    - Adding a debug console to the Scenes [possibly bugged]
    - Made some changes to the formatting of the header guards
    - Updated constants to predefine a list of strings

## [1.1.7] - 2022-08-29
  ### General
    - [Personal] Got the project working on my secondary laptop
    - [Personal] Got c++ linter working on secondary laptop
    - [TODO] do the same on main laptop
    - Added some updates to make migration of the project between devices easier
    - Change the compilation code a rework may be needed soon
    - Did some further code clean up and Fixed the issues that adding the debug menu caused
    - [Future] There should be a way to load and unload textures to memory
    - Removed added include folders since it seems like the flags work Finished
      + This fixed some linking issues
    - Changed the way the debug is handled, it will now be a part of SceneManager which makes far more scenes
    
## [1.1.8] - 2022-08-29
  ### General
    - Fixed the issue with transition from screens forgot to update the screen manager
    - Did some stylistic clean up on the debug menu

## [1.1.9] - 2022-08-29
  ### General
    - Added the res file to gitignore it shouldn't be There
    - Manually updated the resource file, some adjustment is needed here
    - [X] Changed the Card class to use unique pointers to the unit
    - [X] Change the deck obj to have unique pointers to the cards
    - Added the skeleton for the main menu

## [1.1.10] - 2022-09-02
  ### Changed
    - Change int constants to definitions
    - Renamed the cardpointer definitions
    - Moved tilewidth and height out of constants file
    - Changed how the map height and width works
    - Once again changed the changelog and versioning to confide to the Sematic versioning standards
  ### Removed
    - Removed the use of tuples since its not as needed
    - Removing the unused JSON file until I'm ready to deal with that
  ### Added
    - Added the destructor for Tile
    - Added default variables for each of the game's members
  ### Fixed
    - Type issues with the map int vs uint

