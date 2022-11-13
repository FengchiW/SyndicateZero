import pyray as pr
import json
from .SceneManager import SceneManager


class ResourceManager():
    def __init__(self, sm):
        self.textures: dict(str, pr.Texture) = {}
        self.sounds = {}
        self.music = {}
        self.fonts = {}
        self.locales = {}
        self.sceneManager: SceneManager = sm

    def load_texture(self, path: str) -> pr.Texture:
        if path not in self.textures:
            self.textures[path] = pr.load_texture(path)
        return self.textures[path]

    def load_sound(self, path: str):
        if path not in self.sounds:
            self.sounds[path] = pr.load_sound(path)
        return self.sounds[path]

    def load_music(self, path: str):
        if path not in self.music:
            self.music[path] = pr.load_music_stream(path)
        return self.music[path]

    def load_font(self, path: str, size):
        if path not in self.fonts:
            self.fonts[path] = {}
        if size not in self.fonts[path]:
            self.fonts[path][size] = pr.load_font(path, size)
        return self.fonts[path][size]
    
    def load_locales(self, path: str):
        if path not in self.locales:
            try:
                self.locales[path] = json.loads(pr.load_file_text(path))
            except json.JSONDecodeError:
                self.sceneManager.logMessage("Failed to load locale!", 2)
        return self.locales[path]

    def unload_texture(self, path: str):
        if path in self.textures:
            pr.unload_texture(self.textures[path])
            del self.textures[path]

    def unload_sound(self, path: str):
        if path in self.sounds:
            pr.unload_sound(self.sounds[path])
            del self.sounds[path]

    def unload_music(self, path: str):
        if path in self.music:
            pr.unload_music_stream(self.music[path])
            del self.music[path]
