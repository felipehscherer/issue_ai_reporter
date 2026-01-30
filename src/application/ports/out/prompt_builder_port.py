from abc import ABC, abstractmethod

from src.domain.models import Card, Prompt
from src.domain.value_objects import ReportType


class PromptBuilderPort(ABC):
    @abstractmethod
    def build_prompt(self, card: Card, report_type: ReportType) -> Prompt:
        raise NotImplementedError
