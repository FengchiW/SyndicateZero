// Copyright [2022] <Wilson F Wang>

#ifndef SRC_GAMETOOLS_CONSTANTS_H_
#define SRC_GAMETOOLS_CONSTANTS_H_

const int SCREENWIDTH = 1200;
const int SCREENHEIGHT = 600;
const int MAPWIDTH = 10;
const int MAPHEIGHT = 4;
const int OFFSET = 2;
const int TILEWIDTH = SCREENWIDTH / (MAPWIDTH + 2 * OFFSET);
const int TILEHEIGHT = SCREENHEIGHT / 7;

#define StrList std::vector<std::string>

#endif  // SRC_GAMETOOLS_CONSTANTS_H_
