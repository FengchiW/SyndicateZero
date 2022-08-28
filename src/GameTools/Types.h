// Copyright [2022] <Wilson F Wang>

#ifndef SRC_GAMETOOLS_TYPES_H_
#define SRC_GAMETOOLS_TYPES_H_

// tiles can be grass, water, mountain, etc.
enum TileType {
    GRASS,
    WATER,
    MOUNTAIN,
    TREE,
    ROCK,
    EMPTY
};

enum TileStatus {
    NORMAL,
    SELECTED,
    HOVERED,
    ATTACKED
};

// units can be warrior, archer, mage
enum UnitType {
    WARRIOR,
    ARCHER,
    MAGE
};

enum CardStates {
    INDECK,
    DISPLAYED,
    DISABLED,
    PLAYED
};

#endif  // SRC_GAMETOOLS_TYPES_H_
