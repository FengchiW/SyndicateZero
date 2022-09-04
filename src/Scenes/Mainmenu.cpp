// Copyright [2022] <Wilson F Wang>

#include <memory>
#include "../../includes/Scenes/Mainmenu.h"
#include "../../includes/Constants.h"
#include "../../includes/Scenes/Game.h"
#include "../../includes/Scenes/SceneManager.h"

MainMenu::MainMenu(SceneManager* sm) : Scene(sm) {
    // Create Buttons
    Button playButton = { { 0, 0, 200, 50 }, "Play", WHITE };
    Button quitButton = { { 0, 0, 200, 50 }, "Quit", WHITE };

    // Add Buttons to Vector
    buttons.push_back(playButton);
    buttons.push_back(quitButton);

    // Set Button Positions
    for (int i = 0; i < buttons.size(); i++) {
        buttons[i].rect.x = (GetScreenWidth() - buttons[i].rect.width) / 2;
        buttons[i].rect.y = (GetScreenHeight() - buttons[i].rect.height) / 2 + (i * 100);
    }
}

void MainMenu::draw() {
    ClearBackground(BLACK);
    // Syndicate Zero Text
    DrawText("Syndicate Zero", 100, 100, 100, WHITE);

    // Draw Buttons
    for (int i = 0; i < buttons.size(); i++) {
        DrawRectangleRec(buttons[i].rect, buttons[i].color);
        DrawText(buttons[i].text.c_str(), buttons[i].rect.x + 10, buttons[i].rect.y + 10, 20, BLACK);
    }
}

void MainMenu::update([[maybe_unused]] const float dt) {
    // Check if mouse is hovering over buttons
    for (int i = 0; i < buttons.size(); i++) {
        if (CheckCollisionPointRec(GetMousePosition(), buttons[i].rect)) {
            buttons[i].color = LIGHTGRAY;
        } else {
            buttons[i].color = WHITE;
        }
    }
}

void MainMenu::HandleInput() {
    // Check if mouse is clicked
    if (IsMouseButtonPressed(MOUSE_LEFT_BUTTON)) {
        // Check if mouse is hovering over buttons
        for (int i = 0; i < buttons.size(); i++) {
            if (CheckCollisionPointRec(GetMousePosition(), buttons[i].rect)) {
                // Play Button
                if (i == 0) {
                    sceneManager->changeScene(std::make_unique<Game>(sceneManager));
                }
                // Quit Button
                if (i == 1) {
                    exit(0);
                }
            }
        }
    }
}

MainMenu::~MainMenu() {
}
