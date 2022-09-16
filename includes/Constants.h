// Copyright [2022] <Wilson F Wang>

#ifndef INCLUDES_CONSTANTS_H_
#define INCLUDES_CONSTANTS_H_

#include <vector>
#include <string>
#include <memory>

#ifndef VERSION_MAJOR
#define VERSION_MAJOR 0
#endif  // VERSION

#ifndef VERSION_MINOR
#define VERSION_MINOR 0
#endif  // VERSION

#ifndef VERSION_PATCH
#define VERSION_PATCH 0
#endif  // VERSION

#define STRINGIZE2(s) #s
#define STRINGIZE(s) STRINGIZE2(s)
#define VERSION_STRING "v" STRINGIZE(VERSION_MAJOR) \
    "." STRINGIZE(VERSION_MINOR) "." STRINGIZE(VERSION_PATCH)

// Named mapCoord since its between 0 and 65535
typedef unsigned short mapCoord;  // NOLINT
typedef unsigned short ushort;  // NOLINT
typedef std::vector<std::string> StrList;

typedef struct mapCoord2 {
    mapCoord x;
    mapCoord y;
} mapCoord2;

#define UNDEFINED                (static_cast<ushort>(65535))
#define _Default_Screen_Width    (static_cast<ushort>(1200))
#define _Default_Screen_Height   (static_cast<ushort>(600))
#define _Default_MapWidth        (static_cast<mapCoord>(10))
#define _Default_MapHeight       (static_cast<mapCoord>(5))

#endif  // INCLUDES_CONSTANTS_H_
