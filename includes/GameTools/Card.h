// Copyright [2022] <Wilson F Wang>
#ifndef INCLUDES_GAMETOOLS_CARD_H_
#define INCLUDES_GAMETOOLS_CARD_H_

#include <raylib.h>
#include <string>
#include <memory>
#include "Types.h"
#include "../Constants.h"

struct Stats {
  int health;
  int attack;
  int speed;
  int range;
};

// Card class
class Card {
 public:
    Card(mapCoord2 pos, UnitType t,
         int health, int speed, int attack, int range, ushort cost,
         Texture2D UnitTexture,
         Texture2D CardTexture,
         std::string name,
         std::string description,
         CardStates state);
    ~Card() = default;

    // Getters
    mapCoord2 getPos();
    UnitType getUnitType();
    Stats getStats();
    int getCost();
    Texture2D getUnitTexture();
    Texture2D getCardTexture();
    std::string getName();
    std::string getDescription();
    CardStates getState();
    bool hasMoved();

    // Setters
    void setPos(mapCoord2 pos);
    void dealDamage(int damage);

    // Public attributes
    Rectangle collisionBox;
    bool isHovered;
    bool isSelected;
    bool isHeld;

 private:
    CardStates _state;
    std::string _name;
    std::string _description;
    UnitType _type;
    Texture2D _CardTexture;
    Texture2D _UnitTexture;
    Stats _stats;
    mapCoord2 _pos;
    bool _hasMoved;
    bool _hasAttacked;
    ushort _cost;
};

Card* readCard(std::string filename);

typedef std::unique_ptr<Card> Cardpointer;

#endif  // INCLUDES_GAMETOOLS_CARD_H_
