// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include <utility>
#include <memory>
#include "../../includes/Scenes/Game.h"
#include "../../includes/GameTools/Tile.h"
#include "../../includes/GameTools/Card.h"
#include "../../includes/GameTools/Types.h"
#include "../../includes/Constants.h"

Game::Game(SceneManager *sm) : Scene(sm) {
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

  // initialize players
  players[0].mana = turn;
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

      switch (map[i][j]->status) {
      case NORMAL:
        break;
      case HIGHLIGHTED:
        DrawRectangleRec(map[i][j]->rect, BLUE);
        break;
      case HOVERED:
        DrawRectangleRec(map[i][j]->rect, Color{255, 0, 0, 100});
        break;
      default:
        break;
      }

      // draw units on the tile
      // if (map[i][j]->card != nullptr) {
      //   DrawRectangleRec(map[i][j]->card->rect, map[i][j]->card->color);
      // }
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

  // HUD5
  // Draw the current turn
  std::string turnText = "Turn: " + std::to_string(turn);
  DrawText(turnText.c_str(), 10, 10, 20, BLACK);
  // Draw the current player's mana
  std::string manaText = "Mana: " + std::to_string(players[0].mana);
  DrawText(manaText.c_str(), 10, 40, 20, BLACK);
  // Draw the current player's health
  std::string healthText = "Health: " + std::to_string(players[0].health);
  DrawText(healthText.c_str(), 10, 70, 20, BLACK);

  // end turn button
  DrawRectangleRec(endTurnButton, BLACK);

  // Draw the current phase
  std::string phaseText = "Phase: " + phaseToString(phase);
  DrawText(phaseText.c_str(), 10, 100, 20, BLACK);
}

std::string Game::phaseToString(GamePhase phase) {
  switch (phase) {
  case BEGIN:
    return "Summon";
  case ACTION:
    return "Action";
  case END:
    return "End";
  default:
    return "Unknown";
  }
}

void Game::update([[maybe_unused]] const float dt) {}

void Game::endTurn() {
  // end the current phase
  switch (phase) {
  case BEGIN:
    // mana is reset at the beginning of the turn
    players[0].mana = turn;
    // Maybe drawing cards will cost mana?
    players[0].drawCard();
    phase = ACTION;
    break;
  case ACTION:
    phase = END;
    break;
  case END:
    phase = BEGIN;
    // units are reset at the end of the turn
    turn++;
    break;
  default:
    break;
  }
}

void Game::HandleInput() {
  // mouse position
  Vector2 mousePos = GetMousePosition();


  // mouse over map
  for (mapCoord i = 0; i < mapSize.y; i++) {
    for (mapCoord j = 0; j < mapSize.x; j++) {
      if (CheckCollisionPointRec(mousePos, map[i][j]->rect)) {
        // set the tile to hover
        map[i][j]->status = HOVERED;
        if (userHoldingCard != -1) {
          map[i][j]->status = HIGHLIGHTED;
        }
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
    // check if end turn button is clicked
    if (CheckCollisionPointRec(mousePos, endTurnButton)) {
      // end the turn
      endTurn();
    }

    // check if spawning a unit
    if (phase == BEGIN) {
      // check if user is holding a card
      if (userHoldingCard != -1) {
        // if user is on a valid tile
        for (mapCoord i = 0; i < mapSize.y; i++) {
          for (mapCoord j = 0; j < mapSize.x; j++) {
            if (map[i][j]->status == HIGHLIGHTED) {
              // spawn the unit
              map[i][j]->card = std::move(players[0].hand[userHoldingCard]);
              // remove the card from the hand
              players[0].hand.erase(players[0].hand.begin() + userHoldingCard);
              // reset the userHoldingCard
              userHoldingCard = -1;
              // end the turn
              endTurn();
            }
          }
        }
      }
    }

    // check if mouse over any cards in hand
    int handSize = players[0].hand.size();
    userHoldingCard = -1;

    for (int i = 0; i < handSize; i++) {
      players[0].hand[i]->isSelected = false;
      if (CheckCollisionPointRec(mousePos,
                                 players[0].hand[i]->collisionBox)) {
        // set the card to hover
        players[0].hand[i]->isHovered = true;
        if (userHoldingCard == -1) {
          players[0].hand[i]->isSelected = true;
          userHoldingCard = i;
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
  // if (IsMouseButtonReleased(MOUSE_LEFT_BUTTON)) {
  //     // check if mouse over any cards in hand
  //     int handSize = players[0].hand.size();
  //     for (int i = 0; i < handSize; i++) {
  //         // nothing
  //     }
  // }
}

Game::~Game() {
  // delete the map
  for (int i = 0; i < mapSize.x; i++) {
    for (int j = 0; j < mapSize.y; j++) {
      delete map[i][j];
    }
  }
}
