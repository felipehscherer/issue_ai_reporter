from typing import Dict

from src.application.ports.out.ai_client_port import AiClientPort
from src.domain.models import Prompt
from src.infra.clients.gemini_client import GeminiClient


class GeminiAdapter(AiClientPort):
    def __init__(self, config: Dict[str, str], client: GeminiClient | None = None) -> None:
        self._config = config
        self._client = client or GeminiClient(config)

    def generate_text(self, prompt: Prompt) -> str:
        model = self._config.get("model", "gemini-2.5-flash")
        return self._client.generate(prompt.text, model=model)
