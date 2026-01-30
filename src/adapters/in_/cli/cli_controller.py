import argparse

from dotenv import load_dotenv

from src.application.use_cases.generate_report import GenerateReportCommand, GenerateReportUseCase
from src.domain.value_objects import ReportType
from src.adapters.registry.registry_adapter import ConfigRegistry
from src.infra.config.config_loader import load_config


def run_cli() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(prog="issue-ai-reporter")
    subparsers = parser.add_subparsers(dest="command")

    generate = subparsers.add_parser("generate-report", help="Gera relatorio via IA")
    generate.add_argument("--source", required=True, help="Fonte do card (ex: azure, jira)")
    generate.add_argument("--id", required=True, help="ID do card")
    generate.add_argument("--report", default="qa", help="Tipo de relatorio (qa, risks, test_strategy)")
    generate.add_argument("--ai", default="gemini", help="IA (gemini, chatgpt)")
    generate.add_argument("--output-dir", default=None, help="Diretorio de saida do PDF")
    generate.add_argument("--config", default="config/config.json", help="Arquivo de configuracao")

    args = parser.parse_args()
    if args.command != "generate-report":
        parser.print_help()
        return

    config = load_config(args.config)
    registry = ConfigRegistry(config=config)
    use_case = GenerateReportUseCase(registry=registry)

    output_dir = args.output_dir or config.get("defaults", {}).get("output_dir", "outputs")
    pdf_renderer = config.get("defaults", {}).get("pdf_renderer", "fpdf")

    command = GenerateReportCommand(
        source=args.source,
        card_id=str(args.id),
        report_type=ReportType(args.report),
        ai=args.ai,
        output_dir=output_dir,
        pdf_renderer=pdf_renderer,
    )

    use_case.execute(command)
    print("Relatorio gerado com sucesso.")
