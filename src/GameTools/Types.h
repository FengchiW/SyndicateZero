// Copyright [2022] <Wilson F Wang>

#ifndef E__FUTURE_GAME_SRC_GAMETOOLS_TYPES_H_
#define E__FUTURE_GAME_SRC_GAMETOOLS_TYPES_H_

// tiles can be grass, water, mountain, etc.
enum TileType {
    GRASS,
    WATER,
    MOUNTAIN,
    TREE,
    ROCK,
    EMPTY,
    HOVERED
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

#endif  // E__FUTURE_GAME_SRC_GAMETOOLS_TYPES_H_
