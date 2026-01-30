from src.adapters.out.sources.azure_devops_adapter import map_azure_fields_to_card
from src.domain.value_objects import CardType


def test_map_azure_fields_to_card():
    fields = {
        "System.Title": "Teste",
        "System.Description": "Descricao",
        "Microsoft.VSTS.Common.AcceptanceCriteria": "Crits",
    }

    card = map_azure_fields_to_card("123", fields, CardType.STORY, source="azure")

    assert card.card_id == "123"
    assert card.title == "Teste"
    assert card.description == "Descricao"
    assert card.acceptance_criteria == "Crits"
    assert card.card_type == CardType.STORY
    assert card.source == "azure"
