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
    Player(std::string name, int health, int mana);

    // Actions
    void drawCard();
    std::unique_ptr<Card> playCard(int index);
    // void discardCard(std::unique_ptr<Card> card);

    // Getters
    std::vector<std::unique_ptr<Card>> getHand();
    std::vector<std::unique_ptr<Card>> getGraveyard();

    // Setters
    void setDeck(std::stack<std::unique_ptr<Card>> deck);

 private:
    std::string name {};
    int health {};
    int mana {};
    std::stack<std::unique_ptr<Card>> deck;
    std::vector<std::unique_ptr<Card>> graveyard;
    std::vector<std::unique_ptr<Card>> hand;
};

#endif  // INCLUDES_GAMETOOLS_PLAYER_H_
