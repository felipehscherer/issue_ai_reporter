from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from src.domain.models import Report

if TYPE_CHECKING:
    from src.application.use_cases.generate_report import GenerateReportCommand


class GenerateReportInputPort(ABC):
    @abstractmethod
    def execute(self, command: "GenerateReportCommand") -> Report:
        raise NotImplementedError
