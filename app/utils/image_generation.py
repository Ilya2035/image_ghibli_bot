import base64, asyncio, httpx
from typing import Optional
from core.config import settings

REPLICATE_TOKEN = settings.REPLICATE_API_TOKEN
MODEL_VERSION = "407b7fd425e00eedefe7db3041662a36a126f1e4988e6fbadfc49b157159f015"


async def replicate_anime(jpeg: bytes) -> Optional[bytes]:
    headers = {"Authorization": f"Token {REPLICATE_TOKEN}"}
    payload = {
        "version": MODEL_VERSION,
        "input": {
            "image": "data:image/jpeg;base64," + base64.b64encode(jpeg).decode(),
            "prompt": "studio ghibli style portrait, vibrant colors",
            "strength": 0.55,
            "seed": 42
        }
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://api.replicate.com/v1/predictions",
            json=payload, headers=headers, timeout=60
        )
        r.raise_for_status()
        poll_url = r.json()["urls"]["get"]

        while True:
            poll = await client.get(poll_url, headers=headers, timeout=60)
            poll.raise_for_status()
            data = poll.json()
            if data["status"] == "succeeded":
                image_url = data["output"][0]
                break
            if data["status"] == "failed":
                return None
            await asyncio.sleep(2)

        img_bytes = (await client.get(image_url)).content
        return img_bytes
