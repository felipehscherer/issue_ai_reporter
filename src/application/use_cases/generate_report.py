from dataclasses import dataclass
from typing import Dict

from src.application.ports.in_.generate_report_input_port import GenerateReportInputPort
from src.application.ports.out.ai_client_port import AiClientPort
from src.application.ports.out.card_source_port import CardSourcePort
from src.application.ports.out.pdf_renderer_port import PdfRendererPort
from src.application.ports.out.prompt_builder_port import PromptBuilderPort
from src.application.ports.out.registry_port import RegistryPort
from src.domain.models import Report
from src.domain.value_objects import ReportType


@dataclass(frozen=True)
class GenerateReportCommand:
    source: str
    card_id: str
    report_type: ReportType
    ai: str
    output_dir: str
    pdf_renderer: str


class GenerateReportUseCase(GenerateReportInputPort):
    def __init__(self, registry: RegistryPort) -> None:
        self._registry = registry

    def execute(self, command: GenerateReportCommand) -> Report:
        source_adapter = self._resolve_adapter("sources", command.source, CardSourcePort)
        ai_adapter = self._resolve_adapter("ai", command.ai, AiClientPort)
        prompt_builder = self._resolve_adapter("reports", command.report_type.value, PromptBuilderPort)
        pdf_renderer = self._resolve_adapter("renderers", command.pdf_renderer, PdfRendererPort)

        card = source_adapter.fetch_card(command.card_id)
        prompt = prompt_builder.build_prompt(card, command.report_type)
        report_text = ai_adapter.generate_text(prompt)
        pdf_path = pdf_renderer.render(
            report_text,
            metadata={
                "card_id": card.card_id,
                "card_type": card.card_type.value,
                "report_type": command.report_type.value,
                "source": card.source,
                "title": card.title,
            },
            output_dir=command.output_dir,
        )

        return Report(
            text=report_text,
            card_id=card.card_id,
            card_type=card.card_type,
            report_type=command.report_type,
            source=card.source,
        )

    def _resolve_adapter(self, registry_name: str, key: str, expected_type):
        adapter = self._registry.resolve(registry_name, key)
        if not isinstance(adapter, expected_type):
            raise TypeError(
                f"Registro '{registry_name}:{key}' retornou tipo invalido: {type(adapter)}"
            )
        return adapter
