// Copyright [2022] <Wilson F Wang>

#include "Card.h"

Card::Card(int x, int y, UnitType t,
         int health, int speed, int attack, int range,
         Texture2D UnitTexture,
         Texture2D CardTexture,
         std::string name,
         std::string description,
         CardStates state) {
    // initialize the unit
    this->state = state;
    this->name = name;
    this->description = description;
    this->CardTexture = CardTexture;
}
