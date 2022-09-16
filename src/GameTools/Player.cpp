// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include "../../includes/GameTools/Player.h"
#include "../../includes/Constants.h"

Player::Player(std::string name, int health, int mana) {
    // Initialize player
    this->name = name;
    this->health = health;
    this->mana = mana;

    // Initialize deck
    this->deck = std::stack<std::unique_ptr<Card>>();
    this->graveyard = std::vector<std::unique_ptr<Card>>();
    this->hand = std::vector<std::unique_ptr<Card>>();
}

void Player::drawCard() {
    ushort handSize = this->hand.size();
    // Draw a card from the deck
    if (!deck.empty()) {
        // Move the card from the deck to the hand
        // Set the collision box
        deck.top()->collisionBox = Rectangle{
            static_cast<float>(_Default_Screen_Width / 2 - (handSize + 1) * 200 / 2),
            static_cast<float>(_Default_Screen_Height - 100),
            200,
            100};
        hand.push_back(std::move(deck.top()));
        deck.pop();
    }
}
