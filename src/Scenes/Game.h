// Copyright [2022] <Wilson F Wang>

#ifndef E__FUTURE_GAME_SRC_SCENES_GAME_H_
#define E__FUTURE_GAME_SRC_SCENES_GAME_H_

#include <utility>
#include <vector>
#include "SceneManager.h"
#include "../GameTools/Card.h"
#include "../GameTools/Hand.h"
#include "../GameTools/Deck.h"
#include "../GameTools/json.h"
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
    float BoardAnchorX = SCREENWIDTH / 2 - (TILEWIDTH * 4) / 2;
    float BoardAnchorY = SCREENHEIGHT / 2 - (TILEHEIGHT * 2) / 2;
    float BoardPaddingBottom = TILEHEIGHT;
    std::pair<TileType, Card*> map[4][MAPWIDTH];
    std::vector<Card*> units;
    int mx{}, my{};
    unsigned int turn{};
    int lastHoveredTileX{0}, lastHoveredTileY{0};
    bool hasMouseMoved{};
    int playerHealth{}, enemyHealth{};
    Hand hand;
    Deck deck;
};

#endif  // E__FUTURE_GAME_SRC_SCENES_GAME_H_
