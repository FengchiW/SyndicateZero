// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include <stdio.h>
#include "Game.h"
#include "../GameTools/Card.h"
#include "../GameTools/Tile.h"
#include "../GameTools/Types.h"
#include "../GameTools/Constants.h"

Game::Game(SceneManager* sm) : Scene(sm) {
    // initialize map
    for (uint i = 0; i < _Default_MapHeight; i++) {
        for (uint j = 0; j < _Default_MapWidth; j++) {
            map[i][j] = new Tile(
                GRASS,
                NORMAL,
                Rectangle{static_cast<float>(j * TILEWIDTH),
                          static_cast<float>(i * TILEHEIGHT),
                          _Default_Screen_Width / (_Default_MapWidth + 2),
                          _Default_Screen_Height / 7},
                nullptr);
        }
    }
}

void Game::draw() {
    // draw the game map
    for (int i = 0; i < mapHeight; i++) {
        for (int j = 0; j < mapWidth; j++) {
            switch (map[i][j]->type) {
            case GRASS:
                DrawRectangleRec(map[i][j]->rect, GREEN);
                break;
            default:
                DrawRectangleRec(map[i][j]->rect, RED);
                break;
            }

            if (map[i][j]->status == HOVERED) {
                DrawRectangleRec(map[i][j]->rect, Color{255, 0, 0, 100});
            }
        }
    }
}

void Game::update([[maybe_unused]] const float dt) {
    if (hasMouseMoved) {
        // check if mouse is over a tile
        for (int i = 0; i < mapHeight; i++) {
            for (int j = 0; j < mapWidth; j++) {
                if (CheckCollisionPointRec(mousePos, map[i][j]->rect)) {
                    // set the tile to hover
                    map[i][j]->status = HOVERED;
                } else {
                    // set the tile to normal
                    map[i][j]->status = NORMAL;
                }
            }
        }
    }
}

void Game::HandleInput() {
    // mouse position
    Vector2 currentMousePosition = GetMousePosition();

    // check if the mouse has moved
    if (mousePos.x != currentMousePosition.x && mousePos.y != currentMousePosition.y) {
        hasMouseMoved = true;
        mousePos = currentMousePosition;
    }
}

Game::~Game() {
    // delete the map
    for (int i = 0; i < MAPHEIGHT; i++) {
        for (int j = 0; j < MAPWIDTH; j++) {
            delete map[i][j];
        }
    }
}
