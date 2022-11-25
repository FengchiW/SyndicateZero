import pyray as pr
from pyray import Vector2
from pyray import Color


class TextBubble():
    def __init__(self, pos: Vector2, size: Vector2, fontSize: int,
                 Text: str, speed: float = 0) -> None:
        self.rectangle = pr.Rectangle(pos.x, pos.y, size.x, size.y)
        self.fontSize: int = fontSize
        self.speed: float = speed
        self.newText(Text)

    def newText(self, newText: str):
        self.text = newText
        self.textSize = pr.measure_text(self.text, self.fontSize)
        self.lines: list[str] = []
        self.startTime = pr.get_time()
        self.totalTextLength: int = len(newText)
        self.writeDelay: float = self.totalTextLength * self.speed
        self.textLength: int = 0
        brokenStr: list[str] = newText.split(" ")
        curLine: str = ""
        for word in brokenStr:
            textWidth = pr.measure_text(curLine + word, self.fontSize)
            if textWidth < self.rectangle.width - 10:
                curLine += word + " "
            else:
                self.lines.append(curLine)
                curLine = word + " "
        self.lines.append(curLine)

    def draw(self) -> None:
        pr.draw_rectangle_rec(self.rectangle, Color(255, 255, 255, 255))
        pr.draw_rectangle_lines_ex(self.rectangle, 1, Color(0, 0, 0, 255))
        # currentTime = pr.get_time() - self.startTime

        for i, line in enumerate(self.lines):
            pr.draw_text(line, int(self.rectangle.x + 10),
                         int(self.rectangle.y + 10) + (i * (self.fontSize + 1)),
                         self.fontSize, Color(0, 0, 0, 255))
