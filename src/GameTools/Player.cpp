// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include "../../includes/GameTools/Player.h"

Player::Player(std::string name, int health, int mana) {
    // Initialize player
    this->name = name;
    this->health = health;
    this->mana = mana;
}

