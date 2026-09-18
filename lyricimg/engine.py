import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

from .backgrounds import make_background
from .presets import PRESETS, DEFAULT_PRESET

DEFAULT_FONT = os.environ.get(
    "LYRIC_FONT",
    "/System/Library/Fonts/HelveticaNeue.ttc",
)
PADDING_RATIO = 0.08
LINE_SPACING_RATIO = 1.4
TEXT_COLOR = "#ffffff"
SHADOW_COLOR = "#00000066"
SHADOW_OFFSET = 2


def _load_font(size: int, font_path: str | None = None) -> ImageFont.FreeTypeFont:
    path = font_path or DEFAULT_FONT
    if not os.path.exists(path):
        return ImageFont.load_default()
    return ImageFont.truetype(path, size)


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines = []
    for paragraph in text.split("\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            lines.append("")
            continue
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = current + " " + word
            bbox = font.getbbox(candidate)
            if bbox[2] - bbox[0] <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def _fit_font_size(text: str, width: int, height: int, fill: int,
                   font_path: str | None) -> tuple[int, list[str]]:
    padding_x = int(width * PADDING_RATIO)
    padding_y = int(height * PADDING_RATIO)
    usable_w = int((width - 2 * padding_x) * fill / 100)
    usable_h = height - 2 * padding_y

    for size in range(120, 10, -2):
        font = _load_font(size, font_path)
        wrapped = _wrap_text(text, font, usable_w)
        line_h = size * LINE_SPACING_RATIO
        total_h = line_h * len(wrapped)
        if total_h <= usable_h:
            return size, wrapped
    font = _load_font(12, font_path)
    return 12, _wrap_text(text, font, usable_w)


def render_lyric(text: str, preset_name: str = DEFAULT_PRESET,
                 gradient_name: str = "moody", fill: int = 70,
                 font_path: str | None = None,
                 text_color: str = TEXT_COLOR) -> Image.Image:
    preset = PRESETS[preset_name]
    img = make_background(preset.width, preset.height, gradient_name)
    draw = ImageDraw.Draw(img)

    font_size, lines = _fit_font_size(text, preset.width, preset.height, fill, font_path)
    font = _load_font(font_size, font_path)
    line_h = font_size * LINE_SPACING_RATIO
    total_h = line_h * len(lines)

    start_y = (preset.height - total_h) / 2

    for i, line in enumerate(lines):
        if not line:
            continue
        bbox = font.getbbox(line)
        text_w = bbox[2] - bbox[0]
        x = (preset.width - text_w) / 2
        y = start_y + i * line_h
        draw.text((x + SHADOW_OFFSET, y + SHADOW_OFFSET), line,
                  font=font, fill=SHADOW_COLOR)
        draw.text((x, y), line, font=font, fill=text_color)

    return img
