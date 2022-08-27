// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include <stdio.h>
#include "Game.h"
#include "../GameTools/Hand.h"
#include "../GameTools/Deck.h"
#include "../GameTools/json.h"
#include "../GameTools/Card.h"
#include "../GameTools/Types.h"
#include "../GameTools/Constants.h"

Game::Game(SceneManager* sm) : Scene(sm) {
    // initialize map
    for (int i = 0; i < MAPHEIGHT; i++) {
        for (int j = 0; j < MAPWIDTH; j++) {
            map[i][j].first = GRASS;
        }
    }
}

void Game::draw() {
    // draw the game map
    for (int i = 0; i < MAPHEIGHT; i++) {
        for (int j = 0; j < MAPWIDTH; j++) {
            switch (map[i][j].first) {
                case GRASS:
                    DrawRectangle((j+OFFSET) * TILEWIDTH, (i+1) * TILEHEIGHT, TILEWIDTH, TILEHEIGHT, GREEN);
                    break;
                default:
                    DrawRectangle((j+OFFSET) * TILEWIDTH, (i+1) * TILEHEIGHT, TILEWIDTH, TILEHEIGHT, RED);
                    break;
            }
        }
    }

    // draw cards in hand and deck
}

void Game::update([[maybe_unused]] const float dt) {

    if (hasMouseMoved) {
        // check if mouse is over a tile
        int y = mx / TILEWIDTH - OFFSET;
        int x = my / TILEHEIGHT - 1;
        if ( x < MAPHEIGHT && y < MAPWIDTH ) {
            // Mouse is over a tile
            if (lastHoveredTileX != x || lastHoveredTileY != y) {
                // Mouse has moved to a new tile
                map[lastHoveredTileX][lastHoveredTileY].first = GRASS;
                lastHoveredTileX = x;
                lastHoveredTileY = y;
                hasMouseMoved = false;
                map[x][y].first = HOVERED;
                // check if there is a unit on the tile
            }
        } else {
            map[lastHoveredTileX][lastHoveredTileY].first = GRASS;
            hasMouseMoved = false;
        }
    }
}

void Game::HandleInput() {
    // mouse position
    int mouse_x = GetMouseX();
    int mouse_y = GetMouseY();

    // check if the mouse has moved
    if (mouse_x != mx || mouse_y != my) {
        hasMouseMoved = true;
        mx = mouse_x;
        my = mouse_y;
    }
}

Game::~Game() {
    // delete all units in hand and deck
    for (auto unit : units) {
        delete unit;
    }
}
