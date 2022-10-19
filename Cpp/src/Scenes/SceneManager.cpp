// Copyright [2022] <Wilson F Wang>

#include <raylib.h>
#include <utility>
#include "../../includes/Scenes/SceneManager.h"

void SceneManager::logMessage(const std::string &message) {
  consoleMessages.push_back(message);
}

void SceneManager::logError(const std::string &message) {
  consoleMessages.push_back("ERROR: " + message);
}

void SceneManager::logWarning(const std::string &message) {
  consoleMessages.push_back("WARNING: " + message);
}

void SceneManager::clearLog() {
  consoleMessages.clear();
}

StrList SceneManager::getConsoleMessages() const {
  return consoleMessages;
}

void SceneManager::push(std::unique_ptr<Scene> scene) {
  Action action;
  consoleMessages.push_back("LOG: SCENE PUSH ACTION");
  action.type = ActionType::PUSH;
  action.scene = std::move(scene);
  actions.push_back(std::move(action));
}

void SceneManager::pop() {
  Action action;
  consoleMessages.push_back("LOG: SCENE POP ACTION");
  action.type = ActionType::POP;
  actions.push_back(std::move(action));
}

void SceneManager::changeScene(std::unique_ptr<Scene> scene) {
  Action action;
  consoleMessages.push_back("LOG: SCENE REPLACE ACTION");
  action.type = ActionType::REPLACE;
  action.scene = std::move(scene);
  actions.push_back(std::move(action));
}

Scene &SceneManager::peek() { return *scenes.top(); }

void SceneManager::update() {
  for (Action &action : actions) {
    switch (action.type) {
    case ActionType::PUSH:
      scenes.push(std::move(action.scene));
      consoleMessages.push_back("SCENE PUSHED");
      break;
    case ActionType::POP:
      scenes.pop();
      consoleMessages.push_back("SCENE POPPED");
      break;
    case ActionType::REPLACE:
      while (!scenes.empty()) {
        scenes.pop();
        consoleMessages.push_back("SCENE POPPED");
      }
      scenes.push(std::move(action.scene));
      consoleMessages.push_back("SCENE PUSHED");
      break;
    }
  }
  actions.clear();
}

bool SceneManager::isEmpty() const { return scenes.empty(); }

Scene::Scene(SceneManager *_sm) : sceneManager(_sm) {}
