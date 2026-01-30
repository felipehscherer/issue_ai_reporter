from src.application.use_cases.generate_report import GenerateReportCommand, GenerateReportUseCase
from src.application.ports.out.ai_client_port import AiClientPort
from src.application.ports.out.card_source_port import CardSourcePort
from src.application.ports.out.prompt_builder_port import PromptBuilderPort
from src.application.ports.out.pdf_renderer_port import PdfRendererPort
from src.domain.models import Card, Prompt
from src.domain.value_objects import CardType, ReportType


class FakeRegistry:
    def __init__(self, items):
        self._items = items

    def resolve(self, registry_name: str, key: str):
        return self._items[(registry_name, key)]


class FakeSource(CardSourcePort):
    def fetch_card(self, card_id: str) -> Card:
        return Card(
            card_id=card_id,
            title="Titulo",
            description="Descricao",
            acceptance_criteria="Crits",
            card_type=CardType.STORY,
            source="fake",
        )


class FakePrompt(PromptBuilderPort):
    def build_prompt(self, card: Card, report_type: ReportType) -> Prompt:
        return Prompt(text="PROMPT", card_type=card.card_type, report_type=report_type)


class FakeAi(AiClientPort):
    def generate_text(self, prompt: Prompt) -> str:
        return "RELATORIO"


class FakePdf(PdfRendererPort):
    def render(self, text: str, metadata: dict, output_dir: str) -> str:
        return f"{output_dir}/fake.pdf"


def test_generate_report_usecase_flow():
    registry = FakeRegistry(
        {
            ("sources", "azure"): FakeSource(),
            ("ai", "gemini"): FakeAi(),
            ("reports", "qa"): FakePrompt(),
            ("renderers", "fpdf"): FakePdf(),
        }
    )

    use_case = GenerateReportUseCase(registry)
    command = GenerateReportCommand(
        source="azure",
        card_id="1",
        report_type=ReportType.QA,
        ai="gemini",
        output_dir="outputs",
        pdf_renderer="fpdf",
    )

    report = use_case.execute(command)
    assert report.text == "RELATORIO"
    assert report.card_id == "1"
