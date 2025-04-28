from typing import IO
import base64
from openai import AsyncOpenAI
from core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def replicate_image(file: IO[bytes]) -> bytes | None:
    result = await client.images.edit(
        model="gpt-image-1",
        image=[file],
        prompt="Studio Ghibli style portrait",
        n=1,
        size="1024x1024",
    )

    image_base64 = result.data[0].b64_json
    return base64.b64decode(image_base64)
