from typing import Any, Dict

from src.application.ports.out.registry_port import RegistryPort
from src.shared.importer import import_from_path


class ConfigRegistry(RegistryPort):
    def __init__(self, config: Dict[str, Any]) -> None:
        self._config = config

    def resolve(self, registry_name: str, key: str) -> Any:
        registries = self._config.get("registries", {})
        registry = registries.get(registry_name, {})
        class_path = registry.get(key)
        if not class_path:
            raise KeyError(f"Registro '{registry_name}' nao possui a chave '{key}'")

        cls = import_from_path(class_path)

        adapter_config = self._config.get("adapters", {}).get(key, {})
        if registry_name == "reports":
            prompts_dir = self._config.get("prompts", {}).get("dir", "prompts")
            return cls(prompts_dir)
        return cls(adapter_config)
