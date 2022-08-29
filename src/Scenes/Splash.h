// Copyright [2022] <Wilson F Wang>

#ifndef SRC_SCENES_SPLASH_H_
#define SRC_SCENES_SPLASH_H_

#include <utility>
#include <vector>
#include <string>
#include "SceneManager.h"

class SplashScreen final : public Scene {
 public:
    SplashScreen(SceneManager* sceneManager);
    ~SplashScreen();

    void draw() override;
    void update(const float dt) override;
    void HandleInput() override;
};

#endif  // SRC_SCENES_SPLASH_H_
