// Copyright [2022] <Wilson F Wang>

#ifndef SRC_GAMETOOLS_CONSTANTS_H_
#define SRC_GAMETOOLS_CONSTANTS_H_

#define uint unsigned int

#define _Default_Screen_Width    (static_cast<uint>(1200))
#define _Default_Screen_Height   (static_cast<uint>(600))
#define _Default_MapWidth        (static_cast<uint>(10))
#define _Default_MapHeight       (static_cast<uint>(4))

#define StrList                  std::vector<std::string>
#define Cardpointer              std::unique_ptr<Card>

#endif  // SRC_GAMETOOLS_CONSTANTS_H_
