from PIL import Image


GRADIENTS = {
    "pastel": ("#ffecd2", "#fcb69f"),
    "moody": ("#1a1a2e", "#16213e"),
    "sunset": ("#fa709a", "#fee140"),
    "ocean": ("#667eea", "#764ba2"),
    "mint": ("#a8edea", "#fed6e3"),
}

DEFAULT_GRADIENT = "moody"


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def make_gradient(width: int, height: int, color_top: str, color_bottom: str) -> Image.Image:
    top = _hex_to_rgb(color_top)
    bottom = _hex_to_rgb(color_bottom)
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for y in range(height):
        t = y / max(height - 1, 1)
        r = _lerp(top[0], bottom[0], t)
        g = _lerp(top[1], bottom[1], t)
        b = _lerp(top[2], bottom[2], t)
        for x in range(width):
            pixels[x, y] = (r, g, b)
    return img


def make_background(width: int, height: int, gradient_name: str) -> Image.Image:
    color_top, color_bottom = GRADIENTS[gradient_name]
    return make_gradient(width, height, color_top, color_bottom)
