// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include <utility>
#include <memory>
#include "../../includes/Scenes/Game.h"
#include "../../includes/GameTools/Tile.h"
#include "../../includes/GameTools/Card.h"
#include "../../includes/GameTools/Types.h"
#include "../../includes/Constants.h"

Game::Game(SceneManager* sm) : Scene(sm) {
    // initialize map
    for (mapCoord i = 0; i < _Default_MapHeight; i++) {
        for (mapCoord j = 0; j < _Default_MapWidth; j++) {
            map[i][j] = new Tile(
                GRASS,
                NORMAL,
                Rectangle{static_cast<float>(j * tileSize.x),
                          static_cast<float>(i * tileSize.y),
                          _Default_Screen_Width / (_Default_MapWidth + 2),
                          _Default_Screen_Height / 7},
                nullptr);
        }
    }

    // initialize cards
    // Hardcoded for now
    std::unique_ptr<Card> Card_0 = std::unique_ptr<Card>(
        readCard("res/Assets/Cards/0.json"));
    std::unique_ptr<Card> Card_1 = std::unique_ptr<Card>(
        readCard("res/Assets/Cards/0.json"));

    // Add cards to deck
    players[0].deck.push(std::move(Card_0));
    players[0].deck.push(std::move(Card_1));

    // draw the card
    players[0].drawCard();
    players[0].drawCard();
}

void Game::draw() {
    // draw the game map
    for (mapCoord i = 0; i < mapSize.y; i++) {
        for (mapCoord j = 0; j < mapSize.x; j++) {
            switch (map[i][j]->type) {
            case GRASS:
                DrawRectangleRec(map[i][j]->rect, GREEN);
                break;
            default:
                DrawRectangleRec(map[i][j]->rect, RED);
                break;
            }

            if (map[i][j]->status == HOVERED) {
                DrawRectangleRec(map[i][j]->rect, Color{255, 0, 0, 100});
            }
        }
    }

    // draw the player's hand
    int handSize = players[0].hand.size();
    for (int i = 0; i < handSize; i++) {
        // Draw the card
        DrawRectangleRec(players[0].hand[i]->collisionBox, BLUE);
        // Draw the card's text
        DrawText(players[0].hand[i]->getName().c_str(),
                 static_cast<int>(players[0].hand[i]->collisionBox.x + 10),
                 static_cast<int>(players[0].hand[i]->collisionBox.y + 5),
                 20,
                 BLACK);
        // Draw the card's cost
        // get text width
        std::string cost = std::to_string(players[0].hand[i]->getCost());
        int textWidth = MeasureText(cost.c_str(), 20);
        DrawText(cost.c_str(),
                 static_cast<int>(players[0].hand[i]->collisionBox.x + 190 - textWidth),
                 static_cast<int>(players[0].hand[i]->collisionBox.y + 5),
                 20,
                 BLACK);
        // Draw the card's description
        // DrawText(players[0].hand[i]->getDescription().c_str(),
        //          static_cast<int>(players[0].hand[i]->collisionBox.x + 10),
        //          static_cast<int>(players[0].hand[i]->collisionBox.y + 30),
        //          4,
        //          BLACK);
        // Draw the card's attack, speed, health, and range
        Stats stats = players[0].hand[i]->getStats();
        std::string statsString =
            " A: " + std::to_string(stats.attack) +
            " S: " + std::to_string(stats.speed) +
            " H: " + std::to_string(stats.health) +
            " R: " + std::to_string(stats.range);

        DrawText(statsString.c_str(),
                 static_cast<int>(players[0].hand[i]->collisionBox.x + 10),
                 static_cast<int>(players[0].hand[i]->collisionBox.y + 55),
                 20,
                 BLACK);

        // on hover
        if (players[0].hand[i]->isHovered) {
            DrawRectangleRec(players[0].hand[i]->collisionBox, Color{0, 0, 255, 100});
        }

        // is selected
        if (players[0].hand[i]->isSelected) {
            DrawRectangleRec(players[0].hand[i]->collisionBox, Color{0, 255, 0, 100});
        }
    }
}

void Game::update([[maybe_unused]] const float dt) {
}

void Game::HandleInput() {
    // mouse position
    Vector2 mousePos = GetMousePosition();

    for (mapCoord i = 0; i < mapSize.y; i++) {
        for (mapCoord j = 0; j < mapSize.x; j++) {
            if (CheckCollisionPointRec(mousePos, map[i][j]->rect)) {
                // set the tile to hover
                map[i][j]->status = HOVERED;
            } else {
                // set the tile to normal
                map[i][j]->status = NORMAL;
            }
        }
    }

    // check if mouse over any cards in hand
    int handSize = players[0].hand.size();
    for (int i = 0; i < handSize; i++) {
        if (CheckCollisionPointRec(mousePos, players[0].hand[i]->collisionBox)) {
            // set the card to hover
            players[0].hand[i]->isHovered = true;
        } else {
            // set the card to normal
            players[0].hand[i]->isHovered = false;
        }
    }

    // mouse clicked
    if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON)) {
        // check if mouse over any cards in hand
        int handSize = players[0].hand.size();
        bool hasCardBeenSelected = false;
        for (int i = 0; i < handSize; i++) {
            players[0].hand[i]->isSelected = false;
            if (CheckCollisionPointRec(mousePos,
                                         players[0].hand[i]->collisionBox)) {
                // set the card to hover
                players[0].hand[i]->isHovered = true;
                if (!hasCardBeenSelected) {
                    players[0].hand[i]->isSelected = true;
                    hasCardBeenSelected = true;
                } else {
                    players[0].hand[i]->isSelected = false;
                }
            } else {
                // set the card to normal
                players[0].hand[i]->isHovered = false;
            }
        }
    }

    // mouse released
    if (IsMouseButtonReleased(MOUSE_LEFT_BUTTON)) {
        // check if mouse over any cards in hand
        int handSize = players[0].hand.size();
        for (int i = 0; i < handSize; i++) {
            // nothing
        }
    }
}

Game::~Game() {
    // delete the map
    for (int i = 0; i < mapSize.x; i++) {
        for (int j = 0; j < mapSize.y; j++) {
            delete map[i][j];
        }
    }
}
