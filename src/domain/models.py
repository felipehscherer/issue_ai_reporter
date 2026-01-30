from dataclasses import dataclass
from typing import Dict, Optional

from .value_objects import CardType, ReportType


@dataclass(frozen=True)
class Card:
    card_id: str
    title: str
    description: str
    acceptance_criteria: str
    card_type: CardType
    source: str
    raw_fields: Optional[Dict[str, str]] = None


@dataclass(frozen=True)
class Prompt:
    text: str
    card_type: CardType
    report_type: ReportType


@dataclass(frozen=True)
class Report:
    text: str
    card_id: str
    card_type: CardType
    report_type: ReportType
    source: str
