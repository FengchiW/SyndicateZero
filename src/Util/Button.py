import pyray as pr

MENUDISABLEDCOLOR = (50, 50, 50, 255)
MENUACTIVECOLOR = (100, 100, 100, 255)
MENUHOVEREDCOLOR = (200, 200, 200, 255)
MENUTEXTCOLOR = (255, 255, 255, 255)
MENUTEXTHOVEREDCOLOR = (0, 0, 0, 255)
MENUTEXTDISABLEDCOLOR = (100, 100, 100, 255)


class Button():
    def __init__(self, x, y, width, height,
                 text, callback, isDisabled=False) -> None:
        self.rectangle = pr.Rectangle(x, y, width, height)
        self.text = text
        self.textSize = pr.measure_text(self.text, 20)
        self.callback = callback
        self.isDisabled = isDisabled
        self.isHovered = False

    def draw(self) -> None:
        textX = int(
            self.rectangle.x +
            (self.rectangle.width // 2) -
            (self.textSize // 2)
        )
        textY = int(self.rectangle.y + (self.rectangle.height // 2) - 10)
        if self.isHovered:
            pr.draw_rectangle_rec(self.rectangle, MENUHOVEREDCOLOR)
            pr.draw_text(self.text, textX,
                         textY, 20, MENUTEXTHOVEREDCOLOR)
        elif self.isDisabled:
            pr.draw_rectangle_rec(self.rectangle, MENUDISABLEDCOLOR)
            pr.draw_text(self.text, textX,
                         textY, 20, MENUTEXTDISABLEDCOLOR)
        else:
            pr.draw_rectangle_rec(self.rectangle, MENUACTIVECOLOR)
            pr.draw_text(self.text, textX,
                         textY, 20, MENUTEXTCOLOR)

    def is_mouse_over(self, mouse) -> bool:
        if (self.isDisabled):
            return False
        if (pr.check_collision_point_rec(mouse, self.rectangle)):
            self.isHovered = True
            return True
        self.isHovered = False
        return False

    def handle_input(self, mouse):
        if (self.isDisabled):
            return
        if (self.is_mouse_over(mouse) and
                pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON)):
            self.callback()
