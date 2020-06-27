import pygame


class Display:
    def __init__(self):
        pass

    def set_Display_Info(self, name, stats):
        self.stats = stats
        self.name = name

    def draw_Hud(self, win):
        w = win.get_width()
        h = win.get_height()
        HUD_box = pygame.Rect(0, 4*h/5, w, h/5)
        pygame.draw.rect(win, (100, 100, 255), HUD_box, 0)

    def Camera(self):
        pass
