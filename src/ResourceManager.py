import pyray as pr
from typing import TYPE_CHECKING, Any
import json
from enum import Enum
from .util import Card, Map
if TYPE_CHECKING:
    from SceneManager import SceneManager


class ResourceType(Enum):
    TEXTURE = 0
    MAP = 1
    CARD = 2
    SOUND = 3
    MUSIC = 4
    FONT = 5
    LOCALE = 6


class Resource:
    def __init__(self, name: str, path: str, Type: ResourceType) -> None:
        self.name: str = name
        self.path: str = path
        self.Type: ResourceType = Type


class ResourceManager():
    def __init__(self, sceneManager: 'SceneManager') -> None:
        self.textures: dict[str, pr.Texture] = {}
        self.maps:     dict[str, Map] = {}
        self.cards:    dict[str, Card] = {}
        self.sounds:   dict[str, pr.Sound] = {}
        self.music:    dict[str, pr.Music] = {}
        self.fonts:    dict[str, pr.Font] = {}
        self.locales:  dict[str, Any] = {}
        self.sm:       'SceneManager' = sceneManager

        self.load_texture('assets/missing.png', 'missing')
        self.load_font('assets/Roboto-Regular.ttf', 'missing')
        self.load_card('Data/Cards/missing.json', 'missing')

    def load_resource(self, resource: Resource) -> None:
        if resource.Type == ResourceType.TEXTURE:
            self.load_texture(resource.path, resource.name)
        elif resource.Type == ResourceType.MAP:
            self.load_map(resource.path, resource.name)
        elif resource.Type == ResourceType.CARD:
            self.load_card(resource.path, resource.name)
        elif resource.Type == ResourceType.SOUND:
            self.load_sound(resource.path, resource.name)
        elif resource.Type == ResourceType.MUSIC:
            self.load_music(resource.path, resource.name)
        elif resource.Type == ResourceType.FONT:
            self.load_font(resource.path, resource.name)
        elif resource.Type == ResourceType.LOCALE:
            self.load_locale(resource.path, resource.name)
        else:
            self.sm.logMessage(f"Unknown resource type: {resource.Type}")

    def fetch_card(self, key: str) -> Card:
        if key in self.cards:
            return self.cards[key]
        return self.cards['missing']

    def fetch_map(self, key: str) -> Map:
        return self.maps[key]

    def fetch_texture(self, key: str) -> pr.Texture:
        if key in self.textures:
            return self.textures[key]
        return self.textures['missing']

    def fetch_font(self, key: str) -> pr.Font:
        if key in self.fonts:
            return self.fonts[key]
        return self.fonts['missing']

    def fetch_music(self, key: str) -> pr.Music:
        if key in self.music:
            return self.music[key]
        return self.music[key]

    def load_texture(self, path: str, key: str) -> None:
        if key not in self.textures:
            if pr.file_exists(path):
                self.textures[key] = pr.load_texture(path)
                self.sm.logMessage(f"Loaded texture {key} from {path}")
            else:
                self.sm.logMessage(f"Failed to load texture {path}", 2)

    def load_sound(self, path: str, key: str) -> None:
        if path not in self.sounds:
            self.sounds[path] = pr.load_sound(path)

    def load_music(self, path: str, key: str) -> None:
        if path not in self.music:
            self.music[path] = pr.load_music_stream(path)

    def load_font(self, path: str, key: str) -> None:
        if path not in self.fonts:
            self.fonts[path] = pr.load_font(path)

    def load_locale(self, path: str, key: str) -> None:
        # Nothing yet
        pass

    def load_card(self, path: str, key: str) -> None:
        if (key not in self.textures):
            if (pr.file_exists(path)):
                self.cards[key] = Card(json.loads(pr.load_file_text(path)))
                self.sm.logMessage(f"Loaded card {key} from {path}")
            else:
                self.sm.logMessage(f"Failed to load card {path}", 2)

    def load_map(self, path: str, key: str) -> None:
        if key not in self.maps:
            if pr.file_exists(path):
                self.maps[key] = Map(json.loads(pr.load_file_text(path)))
                self.sm.logMessage(f"Loaded map {key} from {path}")
            else:
                self.sm.logMessage(f"Failed to load map {path}", 2)

    def unload_texture(self, key: str) -> None:
        if key in self.textures:
            pr.unload_texture(self.textures[key])
            del self.textures[key]

    def unload_sound(self, key: str) -> None:
        if key in self.sounds:
            pr.unload_sound(self.sounds[key])
            del self.sounds[key]

    def unload_music(self, key: str) -> None:
        if key in self.music:
            pr.unload_music_stream(self.music[key])
            del self.music[key]
