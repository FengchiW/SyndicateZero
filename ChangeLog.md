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

## [1.2.0] - 2022-09-03

### Changed

    - Changed some Type definitions to be typedefs instead of defines
    - Moved build tools to their own folder
    - Moved all the includes to their own folder
      + this broke all the dynamic imports

### Fixed

    - A lot of the statical imports
    - Continued to resolve lint errors
    - Fixed all the include issues
    - Changed the incorrect header guards
    - Fixed issues with symbol linking

### Added

    - New structure uint2 that has two uint position values
    - A make file to make compile times much faster and debugging easier

### Deprecated

    - buildtools folder, both the packager and compile.bat
      + Packager will return but with different functionality

## [1.2.1] - 2022-09-04

### Added

    - Player Class to house the player objects
    - Added setters and getters to the player class
    - A Main Menu
    - RapidJSON library to read write player data

### Fixed

    - So issues with debug menu not displaying

### Changed

    - How debug messages are logged into the console
    - Modified the make file so it now sets the version for the game

## [1.2.2] - 2022-09-09

### Added

    - Added the environment files
    - Added a method to read unit files
    - Added a rectangle to the card class
    - Added the card into the world
    - Added the ability to select cards

### Fixed

    - Rapid json loading for the card
    - Many issues relating to the unique pointers for the player object

### Changed

    - Changed how the unit and card classes function
    - How a bunch of memory management is handled
    - Moved input handling out of update loop into HandleInput

## [1.2.4] - 2022-09-15

### Added

    - A Python version to simplify development

## [1.3.0] - 2022-11-13

### Added

    - New scenes, selections for leaders
    - New backgrounds for the main menu
    - New resource manager so that in the future I can implement some loading logic
    - New way of handling debugging

### Changed

    - Almost everything about the file structure
    - Setting up code for future improvements

### Enhancements

    - Added stronger typing hints for some of the classes
    - Improved code readability
    - Improved the button class so it can be used in more places

### Fixed

    - Many bugs pertaining to the configuration of the Python env
    - The gapping issue with the tile rectangles for the game map

### Removed

    - Removed the current way Cards and Units are implemented

### Todo

    - Move C++ version outside of current branch so that the code is more clean
    - Redesign how the card and unit system works

## [1.0.1] - 2022-11-13

### Added

    - Added an auto Updating tool

### Fixed

    - Fixed all the python importing issues caused by the refactor

### Removed

    - Removed all legacy Cpp code and workspace configurations

### Changed

    - Restarted the versioning system for the python builds!

## [1.1.0] - 2022-11-13

### Added

- Added Units back in
- Added Phases in
- Added basic movement system for units

### Changed

- Changed file structure again

### Fixed

- Fixed bug with movement calculation

### Removed

- Removed some more junk from code

## [1.2.1.1] - 2022-11-14

### Added

- Tool to the updater to produce builds

### Removed

- Removed the unused gitignore rules

## [1.2.2.0] - 2022-11-14

### Changed

- Moved output build into its own place under builds

## [1.2.3.1] - 2022-11-14

### Changed

- Updated the updater again fixed several bugs

## [1.3.0.1] - 2022-11-14

### Added

- Added new threading system to the AI so it doesn't freeze the game

### Fixed

- Fixed issues with call back and buttons

### Removed

- Removed all asyncronous functionallity of the game

## [1.3.0.1] - 2022-11-20

### Added

- Added a lot of new features to the gameplay system
- Added many type hints to improve code readabillity

### Fixed

- Fixed many issues with imports

### Removed

- Removed unneeded asyncronous code

## [1.2.4.1] - 2022-11-20

## [1.3.0.1] - 2022-11-25

### Added

- Added Cards!
- Added Camera

### Changed

- Changed how spawning works to cards spawning

### Fixed

- Fixed issues with scene transitions and circular dependencies

### Removed

- Removed the old way unit spawning worked

## [1.4.0.2] - 2022-12-03

### Added

- Added a map component

### Changed

- Change how the tiles work

### Fixed

- Fixed some issues with movement in the Hexagonal grid

## [1.4.1.2] - 2022-12-03

### Fixed

- Fixed the Updater

## [1.4.2.2] - 2022-12-06

### Added

- Added a new movement mechanic
- Added a map class
- Added the abillity to make maps and read them

### Changed

- The file structure

### Fixed

- Many bugs related to movement

### Removed

- Removed old Movement system

## [1.4.3.3] - 2022-12-07

### Changed

- Moved the file structure for units and cards

### Fixed

- Fixed some more typing issues


## [1.5.0.4] - 2022-12-19
### Added

  - Added new tool tip place holder
  - New tileing system
  - Improved unit movement
  - Loading bar
  - Reconfigured the scene management and resource management
### Changed

  - Change the Scene structure
### Fixed

  - Fixed some bugs with loading resources
