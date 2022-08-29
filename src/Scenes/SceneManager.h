// Copyright [2022] <Wilson F Wang>

#ifndef SRC_SCENES_SCENEMANAGER_H_
#define SRC_SCENES_SCENEMANAGER_H_

#include <vector>
#include <string>
#include <stack>
#include <memory>
#include "../GameTools/Constants.h"

class Scene;

enum class ActionType {
    PUSH,
    POP,
    REPLACE
};

struct Action{
    ActionType type;
    std::unique_ptr<Scene> scene;
};

class SceneManager final {
 public:
    void push(std::unique_ptr<Scene> scene);
    void pop();
    void changeScene(std::unique_ptr<Scene> scene);
    void update();
    Scene& peek();
    bool isEmpty() const;

    StrList consoleMessages;
 private:
    std::stack<std::unique_ptr<Scene>> scenes;
    std::vector<Action> actions;
};

class Scene {
 public:
    explicit Scene(SceneManager* sceneManager);
    virtual ~Scene() = default;

    virtual void update([[maybe_unused]] const float dt) = 0;
    virtual void draw() = 0;
    virtual void HandleInput() = 0;

 protected:
    SceneManager* sceneManager;
};

#endif  // SRC_SCENES_SCENEMANAGER_H_
