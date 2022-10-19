// Copyright [2022] <Wilson F Wang>

#ifndef INCLUDES_SCENES_MAINMENU_H_
#define INCLUDES_SCENES_MAINMENU_H_

#include "SceneManager.h"
#include <raylib.h>
#include <utility>
#include <vector>
#include <string>

class MainMenu final : public Scene {
 public:
    MainMenu(SceneManager* sceneManager);
    ~MainMenu();

    void draw() override;
    void update(const float dt) override;
    void HandleInput() override;

    struct Button {
        Rectangle rect;
        std::string text;
        Color color;
    };

 private:
    std::vector<Button> buttons;
};


#endif  // INCLUDES_SCENES_MAINMENU_H_
