import io
import json
import zipfile

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from lyricimg.backgrounds import GRADIENTS, DEFAULT_GRADIENT
from lyricimg.engine import render_lyric
from lyricimg.presets import PRESETS, DEFAULT_PRESET

app = FastAPI()


@app.post("/api/preview")
async def preview(
    text: str = Form(...),
    preset: str = Form(DEFAULT_PRESET),
    bg: str = Form(DEFAULT_GRADIENT),
    fill: int = Form(70),
):
    img = render_lyric(text, preset_name=preset, gradient_name=bg, fill=fill)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@app.post("/api/render")
async def render(
    text: str = Form(...),
    preset: str = Form(DEFAULT_PRESET),
    bg: str = Form(DEFAULT_GRADIENT),
    fill: int = Form(70),
    fmt: str = Form("png"),
):
    img = render_lyric(text, preset_name=preset, gradient_name=bg, fill=fill)
    buf = io.BytesIO()
    if fmt == "webp":
        img.save(buf, format="WEBP", quality=90)
        media = "image/webp"
    else:
        img.save(buf, format="PNG")
        media = "image/png"
    buf.seek(0)
    return StreamingResponse(
        buf, media_type=media,
        headers={"Content-Disposition": f"attachment; filename=lyric.{fmt}"},
    )


@app.post("/api/render-all")
async def render_all(
    records: str = Form(...),
    preset: str = Form(DEFAULT_PRESET),
    bg: str = Form(DEFAULT_GRADIENT),
    fill: int = Form(70),
):
    lines = json.loads(records)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, text in enumerate(lines, 1):
            img = render_lyric(text, preset_name=preset, gradient_name=bg, fill=fill)
            img_buf = io.BytesIO()
            img.save(img_buf, format="PNG")
            zf.writestr(f"lyric_{i:03d}.png", img_buf.getvalue())
    buf.seek(0)
    return StreamingResponse(
        buf, media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=lyrics.zip"},
    )


@app.get("/api/config")
async def config():
    return {
        "presets": list(PRESETS.keys()),
        "gradients": {k: list(v) for k, v in GRADIENTS.items()},
    }


app.mount("/", StaticFiles(directory="docs", html=True), name="docs")
