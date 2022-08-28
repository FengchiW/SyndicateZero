// Copyright [2022] <Wilson F Wang>

#ifndef SRC_GAMETOOLS_TILE_H_
#define SRC_GAMETOOLS_TILE_H_

struct Tile {
    Tile(int type, int status, Rectangle rect, Card* card);
    int type;
    int status;
    Rectangle rect;
    Card* card;
};

#endif  // SRC_GAMETOOLS_TILE_H_
