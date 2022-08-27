// Copyright [2022] <Wilson F Wang>

#include "Hand.h"

#include <vector>

Hand::Hand() {}

void Hand::add(Card*) {}
void Hand::remove(Card*) {}

void Hand::remove(unsigned int n) {
    if (n >= hand.size()) {
        return;
    }
    hand.erase(hand.begin() + n);
}

Card* Hand::get(unsigned int n) const {
    if (!this->empty()) {
        if (n < this->size()) {
            return this->hand[n];
        }
    }
    return nullptr;
}

unsigned int Hand::size() const {
    return this->hand.size();
}

bool Hand::empty() const {
    return this->hand.empty();
}
