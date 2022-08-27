windres release.rc -O coff -o release.res
g++ -o SyndicateZero.exe src/*.cpp src/Scenes/*.cpp src/GameTools/*.cpp -Wall -Wextra -Werror -std=c++23 -D_DEFAULT_SOURCE -Wno-missing-braces -s -O1 release.res  -I. -IC:/raylib/raylib/src -IC:/raylib/raylib/src/external -L. -LC:/raylib/raylib/src -LC:/raylib/raylib/src -lraylib -lopengl32 -lgdi32 -lwinmm -DPLATFORM_DESKTOP -Wl,--subsystem,windows
SyndicateZero.exe
