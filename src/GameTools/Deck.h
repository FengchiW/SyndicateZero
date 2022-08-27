// Copyright [2022] <Wilson F Wang>
#ifndef E__FUTURE_GAME_SRC_GAMETOOLS_DECK_H_
#define E__FUTURE_GAME_SRC_GAMETOOLS_DECK_H_

#include <vector>
#include "Card.h"

class Deck {
 public:
    Deck();
    void pop();
    void push(Card* u);
    Card* top();
    int size();
    bool empty();
 private:
    std::vector<Card*> deck;
};

#endif  // E__FUTURE_GAME_SRC_GAMETOOLS_DECK_H_
