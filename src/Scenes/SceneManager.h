// Copyright [2022] <Wilson F Wang>

#ifndef E__FUTURE_GAME_SRC_SCENES_SCENEMANAGER_H_
#define E__FUTURE_GAME_SRC_SCENES_SCENEMANAGER_H_

#include <vector>
#include <stack>
#include <memory>

class Scene;

class SceneManager final {
    struct Action{
        enum class Type {
            PUSH,
            POP,
            REPLACE
        };
        Type type;
        std::unique_ptr<Scene> scene;
    };

 public:
    void push(std::unique_ptr<Scene> scene);
    void pop();
    void changeScene(std::unique_ptr<Scene> scene);

    void update();

    Scene& peek();

    bool isEmpty() const;

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
    // virtual void onEnter() = 0;
    // virtual void onExit() = 0;
    // virtual void onPause() = 0;
    // virtual void onResume() = 0;
    virtual void HandleInput() = 0;

 protected:
    SceneManager* sceneManager;
};

#endif  // E__FUTURE_GAME_SRC_SCENES_SCENEMANAGER_H_
