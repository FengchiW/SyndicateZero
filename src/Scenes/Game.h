// Copyright [2022] <Wilson F Wang>

#ifndef SRC_SCENES_GAME_H_
#define SRC_SCENES_GAME_H_

#include <raylib.h>
#include <utility>
#include <memory>
#include <stack>
#include <vector>
#include "SceneManager.h"
#include "../GameTools/Card.h"
#include "../GameTools/Tile.h"
#include "../GameTools/Types.h"
#include "../GameTools/Constants.h"

class Game final : public Scene {
 public:
    Game(SceneManager* sceneManager);
    ~Game();

    void draw() override;
    void update(const float dt) override;
    void HandleInput() override;
 private:
    Tile* map[MAPHEIGHT][MAPWIDTH] = {};
    Vector2 mousePos;
    unsigned int turn{};
    bool hasMouseMoved{};
    int playerHealth{}, enemyHealth{};
    std::stack<std::unique_ptr<Card>> deck;
    std::vector<std::unique_ptr<Card>> hand;
    std::stack<std::unique_ptr<Card>> opponentDeck;
    std::vector<std::unique_ptr<Card>> opponentHand;
};

#endif  // SRC_SCENES_GAME_H_
