from abc import ABC, abstractmethod

from src.domain.models import Card

class CardSourcePort(ABC):
    @abstractmethod
    def fetch_card(self, card_id: str) -> Card:
        raise NotImplementedError
