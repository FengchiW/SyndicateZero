windres release.rc -O coff -o release.res
g++ -o SyndicateZero.exe src/*.cpp src/Scenes/*.cpp src/GameTools/*.cpp -Wall -Wextra -Werror -std=c++17 -D_DEFAULT_SOURCE -Wno-missing-braces -s -O1 release.res -lraylib -lopengl32 -lgdi32 -lwinmm -DPLATFORM_DESKTOP -Wl,--subsystem,windows
SyndicateZero.exe
