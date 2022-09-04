// Copyright [2022] <Wilson F Wang>

#ifndef INCLUDES_GAMETOOLS_TILE_H_
#define INCLUDES_GAMETOOLS_TILE_H_

#include "Card.h"
#include <raylib.h>
#include <memory>

struct Tile {
    Tile(int type, int status, Rectangle rect, std::unique_ptr<Card> card);
    int type;
    int status;
    Rectangle rect;
    std::unique_ptr<Card> card;
};

#endif  // INCLUDES_GAMETOOLS_TILE_H_
