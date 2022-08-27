// Copyright [2022] <Wilson F Wang>

#ifndef E__FUTURE_GAME_SRC_SCENES_SPLASH_H_
#define E__FUTURE_GAME_SRC_SCENES_SPLASH_H_

#include <utility>
#include <vector>
#include "SceneManager.h"

class SplashScreen final : public Scene {
 public:
    SplashScreen(SceneManager* sceneManager);
    ~SplashScreen();

    void draw() override;
    void update(const float dt) override;
    void HandleInput() override;
};

#endif  // E__FUTURE_GAME_SRC_SCENES_SPLASH_H_
