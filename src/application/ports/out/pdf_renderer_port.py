from abc import ABC, abstractmethod
from typing import Dict


class PdfRendererPort(ABC):
    @abstractmethod
    def render(self, text: str, metadata: Dict[str, str], output_dir: str) -> str:
        raise NotImplementedError
