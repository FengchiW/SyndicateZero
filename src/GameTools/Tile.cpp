// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include "Card.h"
#include "Tile.h"

Tile::Tile(int type, int status, Rectangle rect, Card* card) {
    this->type = type;
    this->status = status;
    this->rect = rect;
    this->card = card;
}
