// Copyright [2022] <Wilson F Wang>

#ifndef INCLUDES_CONSTANTS_H_
#define INCLUDES_CONSTANTS_H_

#include <vector>
#include <string>
#include <memory>
#include "GameTools/Card.h"

// Named mapCoord since its between 0 and 65535
typedef unsigned short mapCoord;  // NOLINT
typedef unsigned short ushort;  // NOLINT
typedef std::vector<std::string> StrList;
typedef std::unique_ptr<Card> Cardpointer;
typedef struct mapCoord2 {
    mapCoord x;
    mapCoord y;
} mapCoord2;

#define _Default_Screen_Width    (static_cast<ushort>(1200))
#define _Default_Screen_Height   (static_cast<ushort>(600))
#define _Default_MapWidth        (static_cast<mapCoord>(10))
#define _Default_MapHeight       (static_cast<mapCoord>(4))

#endif  // INCLUDES_CONSTANTS_H_
