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
    Tile* map[_Default_MapHeight]
             [_Default_MapWidth] = {};
    Vector2 mousePos;
    unsigned int turn{0};
    bool hasMouseMoved{false};
    int playerHealth{30}, enemyHealth{30};
    std::stack<std::unique_ptr<Card>> deck;
    std::vector<std::unique_ptr<Card>> hand;
    std::stack<std::unique_ptr<Card>> opponentDeck;
    std::vector<std::unique_ptr<Card>> opponentHand;
    int TILEWIDTH {_Default_Screen_Width / (_Default_MapWidth + 2)};
    int TILEHEIGHT {_Default_Screen_Height / 7};
    Vector2 mapsize {_Default_MapWidth, _Default_MapHeight};
};

#endif  // SRC_SCENES_GAME_H_
