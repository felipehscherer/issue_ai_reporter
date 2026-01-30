from pathlib import Path
from typing import Dict

from src.application.ports.out.prompt_builder_port import PromptBuilderPort
from src.domain.models import Card, Prompt
from src.domain.value_objects import ReportType


class FilePromptBuilder(PromptBuilderPort):
    def __init__(self, prompts_dir: str) -> None:
        self._prompts_dir = Path(prompts_dir)

    def build_prompt(self, card: Card, report_type: ReportType) -> Prompt:
        template_path = self._prompts_dir / report_type.value / f"{card.card_type.value}.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Template nao encontrado: {template_path}")

        template = template_path.read_text(encoding="utf-8")
        content = self._render(template, card)
        return Prompt(text=content, card_type=card.card_type, report_type=report_type)

    def _render(self, template: str, card: Card) -> str:
        raw_fields_text = self._format_raw_fields(card.raw_fields)
        has_raw_fields_placeholder = "{{raw_fields}}" in template
        replacements: Dict[str, str] = {
            "{{card_id}}": card.card_id,
            "{{card_type}}": card.card_type.value,
            "{{title}}": card.title,
            "{{description}}": card.description,
            "{{acceptance_criteria}}": card.acceptance_criteria,
            "{{source}}": card.source,
            "{{raw_fields}}": raw_fields_text,
        }
        for key, value in replacements.items():
            template = template.replace(key, value)
        if not has_raw_fields_placeholder and raw_fields_text:
            template = f"{template}\n\nCampos do card (bruto):\n{raw_fields_text}"
        return template

    def _format_raw_fields(self, raw_fields: Dict[str, str] | None) -> str:
        if not raw_fields:
            return ""
        lines = []
        for key in sorted(raw_fields.keys()):
            value = raw_fields.get(key)
            value_text = str(value).strip() if value is not None else ""
            if not value_text:
                value_text = "Nao informado"
            lines.append(f"- {key}: {value_text}")
        return "\n".join(lines)
