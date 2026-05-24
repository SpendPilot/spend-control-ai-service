from __future__ import annotations

from pathlib import Path

import httpx

from app.core.config import get_settings


class OllamaClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    def ping(self) -> bool:
        try:
            response = httpx.get(f"{self.settings.ollama_base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except httpx.HTTPError:
            return False

    def render(self, prompt_name: str, variables: dict) -> dict:
        prompt_text = Path(__file__).resolve().parents[1] / "prompts" / f"{prompt_name}.txt"
        template = prompt_text.read_text(encoding="utf-8")
        prompt = template.format(**variables)
        try:
            response = httpx.post(
                f"{self.settings.ollama_base_url}/api/generate",
                json={"model": self.settings.ollama_model, "prompt": prompt, "stream": False},
                timeout=self.settings.ollama_request_timeout,
            )
            response.raise_for_status()
            return {"available": True, "text": response.json().get("response", "").strip()}
        except httpx.HTTPError:
            return {"available": False, "text": ""}

