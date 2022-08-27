// Copyright [2022] <Wilson F Wang>

#ifndef E__FUTURE_GAME_SRC_SCENES_MAINMENU_H_
#define E__FUTURE_GAME_SRC_SCENES_MAINMENU_H_

#include "SceneManager.h"

class MainMenu final : public Scene {
 public:
    MainMenu(SceneManager* sceneManager);
    ~MainMenu();

    void draw() override;
    void update(const float dt) override;
    void HandleInput() override;
};


#endif  // E__FUTURE_GAME_SRC_SCENES_MAINMENU_H_
