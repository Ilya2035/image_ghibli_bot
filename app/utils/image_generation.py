import base64
import asyncio
from typing import Optional

import httpx

from core.config import settings

REPLICATE_TOKEN = settings.REPLICATE_API_TOKEN
MODEL_VERSION = (
    "407b7fd425e00eedefe7db3041662a36a126f1e4988e6fbadfc49b157159f015"
)

_client: httpx.AsyncClient | None = None


async def replicate_image(jpeg: bytes) -> Optional[bytes]:

    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            headers={"Authorization": f"Token {REPLICATE_TOKEN}"},
            timeout=60,
            follow_redirects=True,
        )

    payload = {
        "version": MODEL_VERSION,
        "input": {
            "image": "data:image/jpeg;base64," + base64.b64encode(jpeg).decode(),
            "prompt": "studio ghibli style portrait, vibrant colors",
            "strength": 0.55,
            "seed": 42,
        },
    }

    response = await _client.post(
        "https://api.replicate.com/v1/predictions",
        json=payload,
    )
    response.raise_for_status()
    poll_url = response.json()["urls"]["get"]

    while True:
        poll = await _client.get(poll_url)
        poll.raise_for_status()
        data = poll.json()

        if data["status"] == "succeeded":
            image_url = data["output"][0]
            break
        if data["status"] == "failed":
            return None

        await asyncio.sleep(2)

    return (await _client.get(image_url)).content
