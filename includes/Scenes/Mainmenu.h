// Copyright [2022] <Wilson F Wang>

#ifndef INCLUDES_SCENES_MAINMENU_H_
#define INCLUDES_SCENES_MAINMENU_H_

#include "SceneManager.h"

class MainMenu final : public Scene {
 public:
    MainMenu(SceneManager* sceneManager);
    ~MainMenu();

    void draw() override;
    void update(const float dt) override;
    void HandleInput() override;
};


#endif  // INCLUDES_SCENES_MAINMENU_H_
