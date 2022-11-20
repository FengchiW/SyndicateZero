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
        currentScene = sm.scenes[-1]
        currentScene.update(pr.get_frame_time())
        currentScene.draw()
        currentScene.handle_input()
        if sm.debug:
            pr.draw_rectangle_rec(sm.consoleRect, Color(0, 0, 0, 200))
            pr.draw_fps(20, 10)
            ci = sm.shownConsoleMessagesIndex
            for i, msg in enumerate(sm.consoleMessages):
                if (i >= ci and i < ci + 10):
                    pr.draw_text(
                        msg, 20, 20 * (i - ci + 1) + 20,
                        18,
                        Color(150, 255, 255, 255)
                    )

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
