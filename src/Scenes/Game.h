// Copyright [2022] <Wilson F Wang>

#ifndef SRC_SCENES_GAME_H_
#define SRC_SCENES_GAME_H_

#include <raylib.h>
#include <utility>
#include <vector>
#include "SceneManager.h"
#include "../GameTools/Card.h"
#include "../GameTools/Hand.h"
#include "../GameTools/Deck.h"
#include "../GameTools/Tile.h"
#include "../GameTools/json.h"
#include "../GameTools/Types.h"
#include "../GameTools/Constants.h"

class Game final : public Scene {
 public:
    Game(SceneManager* sceneManager, StrList* Console);
    ~Game();

    void draw() override;
    void update(const float dt) override;
    void HandleInput() override;
 private:
    Tile* map[MAPHEIGHT][MAPWIDTH] = {};
    std::vector<Card*> units;
    Vector2 mousePos;
    unsigned int turn{};
    bool hasMouseMoved{};
    int playerHealth{}, enemyHealth{};
    Hand hand;
    Deck deck;
};

#endif  // SRC_SCENES_GAME_H_
