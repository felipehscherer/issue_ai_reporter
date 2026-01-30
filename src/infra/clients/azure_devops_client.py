import os
from typing import Any, Dict

import requests
from requests.auth import HTTPBasicAuth


class AzureDevOpsClient:
    def __init__(self, config: Dict[str, Any]) -> None:
        self._organization = config.get("organization") or os.getenv("AZURE_DEVOPS_ORG")
        self._project = config.get("project") or os.getenv("AZURE_DEVOPS_PROJECT")
        self._pat = config.get("pat") or os.getenv("AZURE_DEVOPS_PAT")
        if not self._organization or not self._project or not self._pat:
            raise ValueError("AZURE_DEVOPS_ORG, AZURE_DEVOPS_PROJECT e AZURE_DEVOPS_PAT sao obrigatorios")

    def get_work_item(self, work_item_id: str) -> Dict[str, Any]:
        url = (
            f"https://dev.azure.com/{self._organization}/"
            f"{self._project}/_apis/wit/workitems/{work_item_id}?api-version=7.0"
        )
        response = requests.get(
            url,
            auth=HTTPBasicAuth("", self._pat),
            headers={"Accept": "application/json"},
            timeout=30,
        )
        if response.status_code != 200:
            raise RuntimeError(f"Erro no Azure: {response.status_code} - {response.text}")
        return response.json()
