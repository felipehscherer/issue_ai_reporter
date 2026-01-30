from src.application.prompting.prompt_builder import FilePromptBuilder
from src.domain.models import Card
from src.domain.value_objects import CardType, ReportType


def test_prompt_builder_replaces_fields(tmp_path):
    prompt_dir = tmp_path / "qa"
    prompt_dir.mkdir(parents=True)
    template = "Titulo: {{title}} - {{card_id}} - {{acceptance_criteria}}"
    (prompt_dir / "story.md").write_text(template, encoding="utf-8")

    card = Card(
        card_id="99",
        title="Titulo X",
        description="Desc",
        acceptance_criteria="C1",
        card_type=CardType.STORY,
        source="azure",
    )

    builder = FilePromptBuilder(str(tmp_path))
    prompt = builder.build_prompt(card, ReportType.QA)

    assert "Titulo X" in prompt.text
    assert "99" in prompt.text
    assert "C1" in prompt.text
