EXEC := SyndicateZero.exe
CC=g++
RAYLIB_FLAGS=-lraylib -lopengl32 -lgdi32 -lwinmm -DPLATFORM_DESKTOP
CCFLAGS=-std=c++17 -D_DEFAULT_SOURCE
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

clean:
	@rm -f $(EXEC) $(GameObj) $(GameToolsObj) $(GameObjectsObj) $(GameStatesObj)
