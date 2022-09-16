// Copyright [2022] <Wilson F Wang>

#ifndef INCLUDES_GAMETOOLS_PLAYER_H_
#define INCLUDES_GAMETOOLS_PLAYER_H_

#include <raylib.h>
#include <string>
#include <vector>
#include <stack>
#include <memory>
#include "Card.h"

// Card class
class Player {
 public:
    // Constructor
    Player(std::string name, int health, int mana);

    // Actions
    void drawCard();
    // void discardCard(std::unique_ptr<Card> card);

    std::stack<std::unique_ptr<Card>> deck;
    std::vector<std::unique_ptr<Card>> graveyard;
    std::vector<std::unique_ptr<Card>> hand;

 private:
    std::string name {};
    int health {};
    int mana {};
};

#endif  // INCLUDES_GAMETOOLS_PLAYER_H_
