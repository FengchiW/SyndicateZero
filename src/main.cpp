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

int main([[maybe_unused]] int argc, [[maybe_unused]] char** argv) {
    // Initialization
    InitWindow(SCREENWIDTH, SCREENHEIGHT, "SyndicateZero");
    SetTargetFPS(120);
    bool __DEBUG_MODE = false;
    //Image logo = LoadImage("res/icon.png");
    //SetWindowIcon(logo);

    SceneManager sceneManager;
    sceneManager.push(std::make_unique<SplashScreen>(&sceneManager));
    sceneManager.update();

    float dt = 0.0f;

    // Main game loop
    while (!WindowShouldClose()) {
        // input
        if(IsKeyPressed(KEY_BACKSLASH)) {
            __DEBUG_MODE = !__DEBUG_MODE;
        }
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
            int currentmessage = 1;
            for (std::string msg : sceneManager.consoleMessages) {
                DrawText(msg.c_str(), 10, 20 + 10 * currentmessage, 10, WHITE);
                currentmessage++;
            }
        }
        EndDrawing();

        sceneManager.update();
    }

    return 0;
}
