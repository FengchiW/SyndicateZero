// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include <memory>
#include <string>
#include "../../includes/Scenes/Splash.h"
#include "../../includes/Scenes/SceneManager.h"
#include "../../includes/Scenes/Game.h"

SplashScreen::SplashScreen(SceneManager* sm) : Scene(sm) {}

void SplashScreen::draw() {
    ClearBackground(BLACK);
    // Draw Title "Syndicate Zero" Centered
    int titleWidth = MeasureText("SZ", 90);
    DrawText("SZ", (GetScreenWidth() - titleWidth) / 2, GetScreenHeight() / 2, 90, YELLOW);

    // Draw Subtitle "A Game by Team Zero" Centered
    int subtitleWidth = MeasureText("v 1.5.5", 20);
    DrawText("v 1.5.5", (GetScreenWidth() - subtitleWidth) / 2, GetScreenHeight() / 2 + 90, 20, WHITE);
}

void SplashScreen::update([[maybe_unused]] const float dt) {
    double time = GetTime();

    // Transition to next scene after 2.5 seconds
    if (time > 2.5f) {
        sceneManager->changeScene(std::make_unique<Game>(sceneManager));
    }
}

void SplashScreen::HandleInput() {
}

SplashScreen::~SplashScreen() {
}
