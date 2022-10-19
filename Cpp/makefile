EXEC := SyndicateZero.exe
CC=g++
VERSION_MAJOR=1
VERSION_MINOR=2
VERSION_PATCH=4
RAYLIB_FLAGS=-lraylib -lopengl32 -lgdi32 -lwinmm -DPLATFORM_DESKTOP
CCFLAGS=  -D_DEFAULT_SOURCE -DVERSION_MAJOR=$(VERSION_MAJOR) \
	-DVERSION_MINOR=$(VERSION_MINOR) -DVERSION_PATCH=$(VERSION_PATCH)
GameTools=$(wildcard src/GameTools/*.cpp)
GameToolsObj=$(patsubst src/GameTools/%.cpp, build/GameTools/%.o, $(GameTools))
GameObjects=$(wildcard src/GameObjects/*.cpp)
GameObjectsObj=$(patsubst src/GameObjects/%.cpp, build/GameObjects/%.o, $(GameObjects))
GameStates=$(wildcard src/Scenes/*.cpp)
GameStatesObj=$(patsubst src/Scenes/%.cpp, build/Scenes/%.o, $(GameStates))
Game=$(wildcard src/*.cpp)
GameObj=$(patsubst src/%.cpp, build/%.o, $(Game))

all: $(EXEC)

debug: CCFLAGS += -Wall -Wextra -DDEBUG -g
debug: $(EXEC)

$(EXEC): $(GameObj) $(GameToolsObj) $(GameObjectsObj) $(GameStatesObj)
	@$(CC) $(GameObj) $(GameToolsObj) $(GameObjectsObj) $(GameStatesObj) -o build/$(EXEC) $(RAYLIB_FLAGS)

$(GameObj): build/%.o: src/%.cpp
	$(CC) -c $< -o $@ $(CCFLAGS)

$(GameToolsObj): build/GameTools/%.o: src/GameTools/%.cpp
	$(CC) -c $< -o $@ $(CCFLAGS)

$(GameObjectsObj): build/GameObjects/%.o: src/GameObjects/%.cpp
	$(CC) -c $< -o $@ $(CCFLAGS)

$(GameStatesObj): build/Scenes/%.o: src/Scenes/%.cpp
	$(CC) -c $< -o $@ $(CCFLAGS)

# build/release.res: src/release.rc
# 	windres -i release.rc -o release.res

clean:
	@rm -f $(EXEC) $(GameObj) $(GameToolsObj) $(GameObjectsObj) $(GameStatesObj)
