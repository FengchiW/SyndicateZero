// Copyright [2022] <Wilson F Wang>
#ifndef INCLUDES_GAMETOOLS_CARD_H_
#define INCLUDES_GAMETOOLS_CARD_H_

#include "Types.h"
#include <raylib.h>
#include <string>
#include <memory>

// Card class
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
    CardStates state;
    std::string name;
    std::string description;
    Texture2D CardTexture;
};

std::unique_ptr<Card> readCard(std::string filename);

#endif  // INCLUDES_GAMETOOLS_CARD_H_
