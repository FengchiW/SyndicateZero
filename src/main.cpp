// Copyright [2022] <Wilson F Wang>
// Game: TitleTBD

#include <string.h>
#include <raylib.h>
#include <stdio.h>
#include <vector>
#include <memory>
#include "Scenes/SceneManager.h"
#include "Scenes/Splash.h"
#include "GameTools/Constants.h"

bool __DEBUG_MODE = true;

int main([[maybe_unused]] int argc, [[maybe_unused]] char** argv) {
    // Initialization
    StrList consoleMessages;

    InitWindow(SCREENWIDTH, SCREENHEIGHT, "SyndicateZero");
    SetTargetFPS(120);
    //Image logo = LoadImage("res/icon.png");
    //SetWindowIcon(logo);

    SceneManager sceneManager;
    sceneManager.push(std::make_unique<SplashScreen>(&sceneManager, &consoleMessages));
    sceneManager.update();

    float dt = 0.0f;

    // Main game loop
    while (!WindowShouldClose()) {
        // Update
        dt = GetFrameTime();
        sceneManager.peek().update(dt);
        sceneManager.peek().HandleInput();
        // Draw
        BeginDrawing();
        ClearBackground(RAYWHITE);
        sceneManager.peek().draw();

        if (__DEBUG_MODE) {
            // draw FPS
            DrawText(("FPS: " + std::to_string(GetFPS())).c_str(), 10, 10, 20, WHITE);
            // draw a Console
            for (std::string msg : consoleMessages) {
                DrawText(msg.c_str(), 10, 30 + consoleMessages.size() * 20, 20, WHITE);
            }
        }

        EndDrawing();
    }

    return 0;
}
