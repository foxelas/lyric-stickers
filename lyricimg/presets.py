from dataclasses import dataclass


@dataclass(frozen=True)
class Preset:
    name: str
    width: int
    height: int


PRESETS = {
    "instagram-story": Preset("instagram-story", 1080, 1920),
    "square": Preset("square", 1080, 1080),
    "instagram-post": Preset("instagram-post", 1080, 1350),
    "signal-sticker": Preset("signal-sticker", 512, 512),
}

DEFAULT_PRESET = "square"
