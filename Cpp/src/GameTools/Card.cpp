// Copyright [2022] <Wilson F Wang>

#include <iostream>
#include <string>
#include <vector>
#include "../../includes/GameTools/Card.h"
#include "../../includes/GameTools/Types.h"
#include "../../includes/rapidjson/document.h"
#include "../../includes/rapidjson/writer.h"
#include "../../includes/rapidjson/stringbuffer.h"

Card::Card(mapCoord2 pos, UnitType t,
           int health, int speed, int attack, int range, ushort cost,
           Texture2D UnitTexture,
           Texture2D CardTexture,
           std::string name,
           std::string description,
           CardStates state) {
  // initialize the unit
  _pos = pos;
  _type = t;
  _stats = {health, speed, attack, range};
  _cost = cost;
  _CardTexture = CardTexture;
  _UnitTexture = UnitTexture;
  _name = name;
  _description = description;
  _state = state;
  _hasMoved = false;
  _hasAttacked = false;
  isHovered = false;
  isSelected = false;
  isHeld = false;
}

std::string Card::getName() {
  return _name;
}

std::string Card::getDescription() {
  return _description;
}

mapCoord2 Card::getPos() {
  return _pos;
}

UnitType Card::getUnitType() {
  return _type;
}

Stats Card::getStats() {
  return _stats;
}

int Card::getCost() {
  return _cost;
}

Texture2D Card::getUnitTexture() {
  return _UnitTexture;
}

Texture2D Card::getCardTexture() {
  return _CardTexture;
}

CardStates Card::getState() {
  return _state;
}

bool Card::hasMoved() {
  return _hasMoved;
}

void Card::setPos(mapCoord2 pos) {
  _pos = pos;
}

void Card::dealDamage(int damage) {
  _stats.health -= damage;
}

// Read card from json file returns a card pointer
// Note: use std::unique_ptr to manage memory
Card *readCard(std::string filename) {
  // read the card from a file
  // open the file
  auto file = LoadFileText(filename.c_str());
  // parse the file
  rapidjson::Document d;
  d.Parse(file);

  // get the card data
  std::string name = d["name"].GetString();
  std::string description = d["description"].GetString();
  int attack = d["attack"].GetInt();
  int health = d["health"].GetInt();
  int speed = d["speed"].GetInt();
  int range = d["range"].GetInt();
  // This should be an enumeration but is an int cause i'm lazy
  int unitType = d["type"].GetInt();

  // std::string cardTexture = d["card-image"].GetString();
  // std::string unitTexture = d["image"].GetString();

  // Create the card
  Card *card = new Card({UNDEFINED, UNDEFINED}, static_cast<UnitType>(unitType),
                        health, speed, attack, range, 0,
                        LoadTexture("res/Assets/Units/placeholder.png"),
                        LoadTexture("res/Assets/Cards/placeholder.png"),
                        name, description, CardStates::IN_HAND);

  UnloadFileText(file);

  return card;
}
