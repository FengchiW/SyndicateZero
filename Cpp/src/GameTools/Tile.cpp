// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include "../../includes/GameTools/Tile.h"
#include "../../includes/GameTools/Card.h"

Tile::Tile(int type, int status, Rectangle rect, std::unique_ptr<Card> card) {
  this->type = type;
  this->status = status;
  this->rect = rect;
  this->card = std::move(card);
}
