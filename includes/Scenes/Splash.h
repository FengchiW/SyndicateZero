// Copyright [2022] <Wilson F Wang>

#ifndef INCLUDES_SCENES_SPLASH_H_
#define INCLUDES_SCENES_SPLASH_H_

#include "SceneManager.h"
#include <utility>
#include <vector>
#include <string>

class SplashScreen final : public Scene {
 public:
    SplashScreen(SceneManager* sceneManager);
    ~SplashScreen();

    void draw() override;
    void update(const float dt) override;
    void HandleInput() override;
};

#endif  // INCLUDES_SCENES_SPLASH_H_
