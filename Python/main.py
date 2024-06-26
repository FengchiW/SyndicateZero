from src import SceneManager, MainMenu
import pyray as pr


def main():
    pr.init_window(1280, 720, "Syndicate Zero")
    pr.set_target_fps(120)
    pr.set_window_icon(pr.load_image("res/icon.png"))

    sm = SceneManager()
    sm.pushScene(MainMenu(sm))

    while not pr.window_should_close():
        pr.begin_drawing()
        pr.clear_background((255, 255, 255, 255))
        currentScene = sm.scenes[-1]
        currentScene.update(pr.get_frame_time())
        currentScene.draw()
        currentScene.handle_input()
        if sm.debug:
            pr.draw_rectangle_rec(sm.consoleRect, (0, 0, 0, 200))
            pr.draw_fps(20, 10)
            ci = sm.shownConsoleMessagesIndex
            for i, msg in enumerate(sm.consoleMessages):
                if (i >= ci and i < ci + 10):
                    pr.draw_text(
                        msg, 20, 20 * (i - ci + 1) + 20,
                        18,
                        (150, 255, 255, 255)
                    )

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
