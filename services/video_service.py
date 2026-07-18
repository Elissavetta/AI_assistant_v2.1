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

        timeout = httpx.Timeout(30.0, connect=10.0, read=60.0)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{self.base_url}/videos",
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
            self.logger.info(f"Video job created: {job.get('id', 'unknown')}")

            self._validate_job_keys(job, ["id", "polling_url", "status"])

            while job.get("status") not in ("completed", "failed"):
                await asyncio.sleep(poll_interval)
                response = await client.get(job["polling_url"], headers=headers)
                response.raise_for_status()
                job = response.json()
                self.logger.info(
                    f"Video job {job.get('id', 'unknown')} status: {job.get('status', 'unknown')}"
                )

            if job["status"] == "failed":
                raise RuntimeError(job.get("error", "Video generation failed"))

            self._validate_job_keys(job, ["unsigned_urls"])
            video_url = job["unsigned_urls"][0]
            video_response = await client.get(video_url, headers=headers)
            video_response.raise_for_status()
            return video_response.content

    def _validate_job_keys(self, job: dict, required_keys: list[str]):
        missing = [k for k in required_keys if k not in job]
        if missing:
            self.logger.error(
                f"API ответ не содержит ожидаемых ключей: {missing}. "
                f"Полученный ответ: {job}"
            )
            raise KeyError(
                f"Неожиданный формат ответа API. Отсутствуют ключи: {missing}"
            )
