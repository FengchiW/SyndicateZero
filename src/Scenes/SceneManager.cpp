// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include <utility>
#include "SceneManager.h"

void SceneManager::push(std::unique_ptr<Scene> scene) {
    Action action;
    action.type = ActionType::PUSH;
    action.scene = std::move(scene);
    actions.push_back(std::move(action));
}

void SceneManager::pop() {
    Action action;
    action.type = ActionType::POP;
    actions.push_back(std::move(action));
}

void SceneManager::changeScene(std::unique_ptr<Scene> scene) {
    Action action;
    action.type = ActionType::REPLACE;
    action.scene = std::move(scene);
    actions.push_back(std::move(action));
}

Scene& SceneManager::peek() { return *scenes.top(); }

void SceneManager::update() {
    for (Action& action : actions) {
        switch (action.type) {
            case ActionType::PUSH:
                scenes.push(std::move(action.scene));
                break;
            case ActionType::POP:
                scenes.pop();
                break;
            case ActionType::REPLACE:
                while (!isEmpty()) {
                    scenes.pop();
                }
                scenes.push(std::move(action.scene));
                break;
        }
    }
    actions.clear();
}

bool SceneManager::isEmpty() const { return scenes.empty(); }

Scene::Scene(SceneManager* _sm) : sceneManager(_sm) {}
