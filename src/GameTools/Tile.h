// Copyright [2022] <Wilson F Wang>

#ifndef SRC_GAMETOOLS_TILE_H_
#define SRC_GAMETOOLS_TILE_H_

#include <memory>

struct Tile {
    Tile(int type, int status, Rectangle rect, std::unique_ptr<Card> card);
    int type;
    int status;
    Rectangle rect;
    std::unique_ptr<Card> card;
};

#endif  // SRC_GAMETOOLS_TILE_H_
