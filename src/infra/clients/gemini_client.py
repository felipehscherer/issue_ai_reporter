import os
from typing import Any, Dict

from google import genai


class GeminiClient:
    def __init__(self, config: Dict[str, Any]) -> None:
        api_key = config.get("api_key") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY e obrigatoria")
        self._client = genai.Client(api_key=api_key)

    def generate(self, prompt: str, model: str) -> str:
        response = self._client.models.generate_content(model=model, contents=prompt)
        return response.text
