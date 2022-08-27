// Copyright [2022] <Wilson F Wang>
#ifndef E__FUTURE_GAME_SRC_GAMETOOLS_HAND_H_
#define E__FUTURE_GAME_SRC_GAMETOOLS_HAND_H_

#include "Card.h"
#include <vector>

// Hand Class
class Hand {
 public:
    Hand();
    ~Hand() = default;
    void add(Card*);
    void remove(Card*);
    void remove(unsigned int);
    Card* get(unsigned int) const;
    unsigned int size() const;
    bool empty() const;
 private:
    std::vector<Card*> hand;
};

#endif  // E__FUTURE_GAME_SRC_GAMETOOLS_HAND_H_
