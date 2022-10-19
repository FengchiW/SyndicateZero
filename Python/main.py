from src import SceneManager, MainMenu
import pyray as pr


def main():
    pr.init_window(800, 450, "Hello")
    pr.set_target_fps(60)

    sm = SceneManager()
    sm.pushScene(MainMenu(sm))

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background((255, 255, 255, 255))
        currentScene = sm.scenes[-1]
        currentScene.update(pr.get_frame_time())
        currentScene.draw()
        currentScene.handle_input()
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
