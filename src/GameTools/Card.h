// Copyright [2022] <Wilson F Wang>
#ifndef E__FUTURE_GAME_SRC_GAMETOOLS_CARD_H_
#define E__FUTURE_GAME_SRC_GAMETOOLS_CARD_H_

#include "Types.h"
#include <raylib.h>
#include <string>

// Unit
struct Unit {
    Unit(int, int, UnitType, int, int, int, int);
    int x;
    int y;
    UnitType t;
    int health;
    int speed;
    int attack;
    int range;
    Texture2D UnitTexture;
};

// Unit Card
class Card {
 public:
    Card(int x, int y, UnitType t,
         int health, int speed, int attack, int range,
         Texture2D UnitTexture,
         Texture2D CardTexture,
         std::string name,
         std::string description,
         CardStates state);
    ~Card() = default;

 private:
    Unit unit;
    CardStates state;
    std::string name;
    std::string description;
    Texture2D CardTexture;
};

#endif  // E__FUTURE_GAME_SRC_GAMETOOLS_CARD_H_
