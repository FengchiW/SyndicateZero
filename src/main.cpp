// Copyright [2022] <Wilson F Wang>
// Game: TitleTBD

#include <string.h>
#include <raylib.h>
#include <stdio.h>
#include <memory>
#include "Scenes/SceneManager.h"
#include "Scenes/Game.h"
#include "GameTools/Constants.h"

bool __DEBUG_MODE;

int main([[maybe_unused]] int argc, [[maybe_unused]] char** argv) {
    // Initialization

    InitWindow(SCREENWIDTH, SCREENHEIGHT, "SyndicateZero");
    SetTargetFPS(120);
    Image logo = LoadImage("res/icon.png");
    SetWindowIcon(logo);

    SceneManager sceneManager;
    sceneManager.push(std::make_unique<Game>(&sceneManager));
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
        EndDrawing();
    }

    return 0;
}
