from abc import ABC, abstractmethod

from src.domain.models import Prompt


class AiClientPort(ABC):
    @abstractmethod
    def generate_text(self, prompt: Prompt) -> str:
        raise NotImplementedError
