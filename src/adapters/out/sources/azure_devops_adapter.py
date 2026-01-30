from typing import Dict

from src.application.ports.out.card_source_port import CardSourcePort
from src.domain.models import Card
from src.domain.value_objects import CardType
from src.infra.clients.azure_devops_client import AzureDevOpsClient


class AzureDevOpsAdapter(CardSourcePort):
    def __init__(self, config: Dict[str, str], client: AzureDevOpsClient | None = None) -> None:
        self._config = config
        self._client = client or AzureDevOpsClient(config)

    def fetch_card(self, card_id: str) -> Card:
        data = self._client.get_work_item(card_id)
        fields = data.get("fields", {})
        card_type = _infer_card_type(fields)
        return map_azure_fields_to_card(card_id, fields, card_type, source="azure")


def map_azure_fields_to_card(
    card_id: str, fields: Dict[str, str], card_type: CardType, source: str
) -> Card:
    title = fields.get("System.Title", "Sem titulo")
    description = fields.get("System.Description", "Nao informado")
    acceptance = fields.get("Microsoft.VSTS.Common.AcceptanceCriteria", "Nao informado")

    return Card(
        card_id=str(card_id),
        title=title,
        description=description,
        acceptance_criteria=acceptance,
        card_type=card_type,
        source=source,
        raw_fields=fields,
    )


def _infer_card_type(fields: Dict[str, str]) -> CardType:
    work_item_type = str(fields.get("System.WorkItemType", "")).strip().lower()
    mapping = {
        "user story": CardType.STORY,
        "story": CardType.STORY,
        "bug": CardType.BUG,
        "task": CardType.TASK,
        "epic": CardType.EPIC,
    }
    return mapping.get(work_item_type, CardType.STORY)
