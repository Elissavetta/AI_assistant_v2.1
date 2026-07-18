import logging
import httpx
import asyncio
from config import Config


class VideoService:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.logger = logging.getLogger(__name__)

    async def generate_video(
        self,
        prompt: str,
        size: str = "1920x1080",
        duration: int = 8,
        poll_interval: int = 5,
    ) -> bytes:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/videos",
                headers=headers,
                json={
                    "model": "veo-3.1-lite",
                    "prompt": prompt,
                    "size": size,
                    "duration": duration,
                },
            )
            response.raise_for_status()
            job = response.json()
            self.logger.info(f"Video job created: {job['id']}")

            while job.get("status") not in ("completed", "failed"):
                await asyncio.sleep(poll_interval)
                response = await client.get(job["polling_url"], headers=headers)
                response.raise_for_status()
                job = response.json()
                self.logger.info(f"Video job {job['id']} status: {job['status']}")

            if job["status"] == "failed":
                raise RuntimeError(job.get("error", "Video generation failed"))

            video_url = job["unsigned_urls"][0]
            video_response = await client.get(video_url, headers=headers)
            video_response.raise_for_status()
            return video_response.content
