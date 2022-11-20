import pyray as pr
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from SceneManager import SceneManager


class Resource():
    def __init__(self, key: str, path: str):
        self.key:  str = key
        self.path: str = path


class ResourceManager():
    def __init__(self, sceneManager: 'SceneManager') -> None:
        self.textures: dict[str, pr.Texture] = {}
        self.sounds:   dict[str, pr.Sound] = {}
        self.music:    dict[str, pr.Music] = {}
        self.fonts:    dict[str, pr.Font] = {}
        self.locales:  dict[str, Any] = {}
        self.sm:       'SceneManager' = sceneManager

    def load_texture(self, path: str, key: str) -> None:
        if key not in self.textures:
            self.textures[key] = pr.load_texture(path)

    def load_sound(self, path: str) -> None:
        if path not in self.sounds:
            self.sounds[path] = pr.load_sound(path)

    def load_music(self, path: str) -> None:
        if path not in self.music:
            self.music[path] = pr.load_music_stream(path)

    def load_font(self, path: str) -> None:
        if path not in self.fonts:
            self.fonts[path] = pr.load_font(path)

    def load_locales(self, path: str) -> None:
        # Nothing yet
        pass

    def unload_texture(self, path: str) -> None:
        if path in self.textures:
            pr.unload_texture(self.textures[path])
            del self.textures[path]

    def unload_sound(self, path: str) -> None:
        if path in self.sounds:
            pr.unload_sound(self.sounds[path])
            del self.sounds[path]

    def unload_music(self, path: str) -> None:
        if path in self.music:
            pr.unload_music_stream(self.music[path])
            del self.music[path]
