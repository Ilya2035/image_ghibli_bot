from __future__ import annotations

import base64
import io
import os
import tempfile
from typing import Optional

from PIL import Image, ImageDraw
from openai import AsyncOpenAI
from core.config import settings


_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


def _make_square_png(jpeg: bytes, size: int = 1024) -> str:
    """JPEG → квадратный PNG нужного размера, сохраняем во временный файл."""
    img = Image.open(io.BytesIO(jpeg)).convert("RGB")
    side = max(img.size)
    canvas = Image.new("RGB", (side, side), (255, 255, 255))
    canvas.paste(img, ((side - img.width) // 2, (side - img.height) // 2))
    canvas = canvas.resize((size, size))

    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    canvas.save(path, "PNG")
    return path


def _make_full_mask(size: int = 1024) -> str:
    """Прозрачная маска PNG `size×size`, разрешающая редактировать всё."""
    mask = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    draw.rectangle([0, 0, size, size], fill=(255, 255, 255, 0))  # всё прозрачно

    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    mask.save(path, "PNG")
    return path


async def ghibli_style_transfer(jpeg: bytes) -> Optional[bytes]:
    """
    Полный цикл: JPEG → square PNG → маска → DALL-E-2 edit → bytes PNG.
    Возвращает None, если API вернул ошибку.
    """
    img_path = _make_square_png(jpeg)
    mask_path = _make_full_mask()

    try:
        with open(img_path, "rb") as img, open(mask_path, "rb") as mask:
            rsp = await _client.images.edit(
                model="dall-e-2",
                image=img,
                mask=mask,
                prompt=(
                    "Repaint the image in the warm, soft aesthetic of a "
                    "Studio Ghibli animated film while preserving the "
                    "person’s face, expression and pose."
                ),
                n=1,
                size="1024x1024",
                response_format="b64_json",
            )
        return base64.b64decode(rsp.data[0].b64_json)
    except Exception as exc:
        print("OpenAI-error:", exc)
        return None
    finally:
        os.remove(img_path)
        os.remove(mask_path)
