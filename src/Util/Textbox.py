import pyray as pr
from pyray import Vector2
from pyray import Color


class Textbox():
    def __init__(self, pos: Vector2, size: Vector2, fontSize: int,
                 charLimit: int = 12, placeholder: str = "",
                 disabled: bool = False) -> None:
        self.placeholder = placeholder
        self.rectangle = pr.Rectangle(pos.x, pos.y, size.x, size.y)
        self.text = ""
        self.fontSize = fontSize
        self.textSize = pr.measure_text(self.text, self.fontSize)
        self.isDisabled = disabled
        self.isHovered = False
        self.isFocused = False
        self.isErrored = False
        self.charLimit = charLimit
        self.textLength = 0

    def draw(self) -> None:
        pr.draw_rectangle_rec(self.rectangle, Color(255, 255, 255, 255))
        pr.draw_rectangle_lines_ex(self.rectangle, 1, Color(0, 0, 0, 255))
        if self.isHovered:
            pr.draw_rectangle_lines_ex(
                self.rectangle, 1, Color(0, 0, 255, 255))
        if self.isFocused:
            pr.draw_rectangle_lines_ex(
                self.rectangle, 1, Color(0, 255, 0, 255))
        if self.isErrored:
            pr.draw_rectangle_lines_ex(
                self.rectangle, 1, Color(255, 0, 0, 255))
        if self.text == "":
            pr.draw_text(self.placeholder, int(self.rectangle.x + 10),
                         int(self.rectangle.y + 10), self.fontSize,
                         Color(100, 100, 100, 255))
        else:
            pr.draw_text(self.text, int(self.rectangle.x + 10),
                         int(self.rectangle.y + 10), self.fontSize,
                         Color(0, 0, 0, 255))

    def is_mouse_over(self, mouse: Vector2) -> bool:
        if self.isDisabled:
            return False
        if pr.check_collision_point_rec(mouse, self.rectangle):
            self.isHovered = True
            return True
        self.isHovered = False
        return False

    def handle_input(self, mouse: Vector2):
        if self.isDisabled:
            return
        if self.is_mouse_over(mouse):
            if pr.is_mouse_button_pressed(pr.MOUSE_LEFT_BUTTON):
                self.isFocused = True
            elif pr.is_mouse_button_pressed(pr.MOUSE_RIGHT_BUTTON):
                self.isFocused = False
        if self.isFocused:
            if pr.is_key_pressed(pr.KEY_BACKSPACE):
                if self.textLength > 0:
                    self.text = self.text[:-1]
                    self.textLength -= 1
                    self.isErrored = False
            else:
                keypressed = pr.get_key_pressed()
                if keypressed >= 65 and keypressed <= 90:
                    if self.textLength < self.charLimit:
                        self.text += chr(keypressed)
                        self.textLength += 1
                    else:
                        self.isErrored = True
