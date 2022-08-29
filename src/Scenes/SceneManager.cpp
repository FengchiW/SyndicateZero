// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include <utility>
#include "SceneManager.h"

void SceneManager::push(std::unique_ptr<Scene> scene) {
    Action action;
    action.type = Action::Type::PUSH;
    action.scene = std::move(scene);
    actions.push_back(std::move(action));
}

void SceneManager::pop() {
    Action action;
    action.type = Action::Type::POP;
    actions.push_back(std::move(action));
}

void SceneManager::changeScene(std::unique_ptr<Scene> scene) {
    Action action;
    action.type = Action::Type::REPLACE;
    action.scene = std::move(scene);
    actions.push_back(std::move(action));
}

Scene& SceneManager::peek() { return *scenes.top(); }

void SceneManager::update() {
    for (Action& action : actions) {
        switch (action.type) {
            case Action::Type::PUSH:
                scenes.push(std::move(action.scene));
                break;
            case Action::Type::POP:
                scenes.pop();
                break;
            case Action::Type::REPLACE:
                while (!scenes.empty()) {
                    scenes.pop();
                }
                scenes.push(std::move(action.scene));
                break;
        }
    }
    actions.clear();
}

bool SceneManager::isEmpty() const { return scenes.empty(); }

Scene::Scene(SceneManager* _sm, std::vector<std::string>* _cm)
: sceneManager(_sm), consoleMessages(_cm) {}
