// Copyright [2022] <Wilson F Wang>

#ifndef INCLUDES_SCENES_GAME_H_
#define INCLUDES_SCENES_GAME_H_

#include <raylib.h>
#include <utility>
#include <memory>
#include <stack>
#include <vector>
#include <string>
#include "SceneManager.h"
#include "../GameTools/Card.h"
#include "../GameTools/Tile.h"
#include "../GameTools/Types.h"
#include "../Constants.h"
#include "../GameTools/Player.h"

enum GamePhase {
    BEGIN,
    ACTION,
    END
};

class Game final : public Scene {
 public:
    Game(SceneManager* sceneManager);
    ~Game();

    void draw() override;
    void update(const float dt) override;
    void HandleInput() override;

    void endTurn();
    std::string phaseToString(GamePhase phase);

 private:
    Tile* map[_Default_MapHeight]
             [_Default_MapWidth] = {};
    unsigned int turn{0};
    Player players[2] {Player("Player 1", 20, 0),
                       Player("Alan", 20, 0)};
    mapCoord2 tileSize {_Default_Screen_Width / (_Default_MapWidth + 2),
                        _Default_Screen_Height / 7};
    mapCoord2 mapSize {_Default_MapWidth, _Default_MapHeight};
    GamePhase phase {BEGIN};
    Rectangle endTurnButton {static_cast<float>(_Default_Screen_Width - 200),
                             static_cast<float>(_Default_Screen_Height - 100),
                             200, 100};
    int userHoldingCard {-1};
};

#endif  // INCLUDES_SCENES_GAME_H_
