// Copyright [2022] <Wilson F Wang>

#include "Deck.h"

Deck::Deck() {}
void Deck::pop() {
    if (!this->empty()) {
        this->deck.pop_back();
    }
}

void Deck::push(Card* u) {
    this->deck.push_back(u);
}

Card* Deck::top() {
    if (!this->empty()) {
        return this->deck.back();
    }
    return nullptr;
}

int Deck::size() {
    return this->deck.size();
}

bool Deck::empty() {
    return this->deck.empty();
}
