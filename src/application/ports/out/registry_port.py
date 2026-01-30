from abc import ABC, abstractmethod
from typing import Any


class RegistryPort(ABC):
    @abstractmethod
    def resolve(self, registry_name: str, key: str) -> Any:
        raise NotImplementedError
