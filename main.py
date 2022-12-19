from src import SceneManager
from src.Scenes.MainMenu import MainMenu
import pyray as pr
from src import Constants
from pyray import Color


def main():
    pr.init_window(Constants.DEFAULT_SCREEN_WIDTH,
                   Constants.DEFAULT_SCREEN_HEIGHT, "Syndicate Zero")
    pr.set_target_fps(120)
    pr.set_window_icon(pr.load_image("res/icon.png"))

    sm = SceneManager()
    sm.pushScene(MainMenu(sm))

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background(Color(255, 255, 255, 255))
        sm.run()
        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
