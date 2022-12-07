from pyray import Vector2, Image
from typing import Optional
from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, position: Vector2, texture: Optional[Image] = None):
        self.position: Vector2 = position
        self.isHovered: bool = False
        self.isSelectable: bool = False
        self.isSelected: bool = False
        # self.texture: pr.Image = None

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update(self, deltaTime: float) -> None:
        pass
