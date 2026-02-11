# Issue AI Reporter (CLI)

Ferramenta CLI para gerar relatorios de qualidade a partir de cards de ferramentas de gestao, usando IA.  
O sistema segue Clean Architecture + Ports & Adapters, com foco em extensibilidade, testabilidade e baixo acoplamento.

## Objetivo

- Ler um card (ex: Azure DevOps, Jira)
- Extrair campos relevantes
- Montar um prompt baseado em tipo de card + tipo de relatorio
- Enviar para uma IA
- Gerar PDF com o resultado

## Arquitetura (resumo)

- **Dominio**: modelos e regras de negocio (Card, Report, Prompt)
- **Aplicacao**: casos de uso (GenerateReportUseCase)
- **Ports**: interfaces para fontes, IA, prompts, PDF e registry
- **Adapters**: Azure/Jira, Gemini/ChatGPT, PDF, CLI
- **Infra**: SDKs, clients HTTP, libs de PDF

## Estrutura do projeto

```
src/
  domain/
    models.py
    value_objects.py
  application/
    use_cases/
    ports/
      in/
      out/
  adapters/
    in_/cli/
    out/sources/
    out/ai/
    out/pdf/
    registry/
  infra/
    clients/
    config/
prompts/
  qa/
  risks/
  test_strategy/
tests/
  unit/
  integration/
```

## Como rodar

1) Instalar dependencias:
```
pip install -r requirements.txt
```

2) Definir variaveis de ambiente:
- `AZURE_DEVOPS_ORG`
- (Opcional) `AZURE_DEVOPS_ORG_URL` (URL completa da org, ex: `https://dev.azure.com/<org>` ou `https://<org>.visualstudio.com`)
- `AZURE_DEVOPS_PROJECT`
- `AZURE_DEVOPS_PAT`
- `GEMINI_API_KEY`

3) Executar:
```
python main.py generate-report --source azure --id 359337 --report qa --ai gemini
```

Opcional:
- `--output-dir` (pasta de saida)
- `--config` (arquivo de configuracao)

## Fluxo CLI

Exemplo:
```
python main.py generate-report --source azure --id 359337 --report qa --ai gemini
```

Passos internos:
1. CLI valida argumentos e cria o comando do caso de uso
2. Use case resolve `source`, `ai` e `prompt_builder` via registry
3. Card e parseados para o modelo de dominio
4. Prompt e montado com base em `card_type + report_type`
5. IA gera o texto do relatorio
6. PDF e gerado e salvo

## Configuracao

O sistema usa registries para extensao sem alterar o core:

- `SOURCE_REGISTRY`: Azure, Jira, etc
- `AI_REGISTRY`: Gemini, ChatGPT, etc
- `REPORT_TYPE_REGISTRY`: QA, Riscos, Estrategia, etc

Cada registro mapeia uma chave para uma classe/adapter.

Exemplo em `config/config.json`:
```
{
  "registries": {
    "sources": {
      "azure": "src.adapters.out.sources.azure_devops_adapter.AzureDevOpsAdapter"
    },
    "ai": {
      "gemini": "src.adapters.out.ai.gemini_adapter.GeminiAdapter"
    },
    "reports": {
      "qa": "src.application.prompting.prompt_builder.FilePromptBuilder"
    },
    "renderers": {
      "fpdf": "src.adapters.out.pdf.fpdf_adapter.FpdfRendererAdapter"
    }
  }
}
```

## Prompts (sem hardcode)

- Templates ficam em `prompts/`
- Um prompt e selecionado por `card_type + report_type`
- O `PromptBuilder` carrega o template e injeta dados do Card

Exemplo de estrutura:
```
prompts/
  qa/
    story.md
    bug.md
  risks/
    story.md
  test_strategy/
    epic.md
```

## Como adicionar novas implementacoes

### Nova IA
1. Criar um adapter que implemente `AiClientPort`
2. Registrar em `registries.ai` no `config/config.json`
3. (Opcional) Adicionar configuracao de modelo/parametros no config

### Nova fonte (Jira)
1. Criar um adapter que implemente `CardSourcePort`
2. Mapear campos do Jira para o modelo `Card`
3. Registrar em `registries.sources`

### Novo tipo de relatorio
1. Criar um `PromptBuilder` para o novo tipo
2. Criar templates em `prompts/<tipo>/`
3. Registrar em `registries.reports`

### Novo tipo de card (Bug, Task, Epic)
1. Definir o novo `CardType` no dominio
2. Ajustar o parser/mapeamento da fonte
3. Criar templates por relatorio (se necessario)

## Onde editar work type (card type)

O tipo do card agora e inferido automaticamente a partir do campo do Azure:
- **Inferencia do tipo**: `src/adapters/out/sources/azure_devops_adapter.py` (funcao `_infer_card_type`)
- **Enum de tipos suportados**: `src/domain/value_objects.py` (`CardType`)

Se quiser mapear um novo work item type do Azure, adicione no `mapping` de `_infer_card_type`.

## Onde editar modelos de IA

- **Adapter de IA (Gemini)**: `src/adapters/out/ai/gemini_adapter.py`
- **Cliente HTTP do Gemini**: `src/infra/clients/gemini_client.py`
- **Registry de IA**: `config/config.json` em `registries.ai`

Para adicionar outra IA, crie um adapter que implemente `AiClientPort` e registre em `config/config.json`.

## Onde editar tudo (pontos principais)

- **Prompts (texto e estrutura)**: `prompts/<report_type>/<card_type>.md`
- **Campos do card (parse + raw fields)**: `src/adapters/out/sources/azure_devops_adapter.py`
- **Montagem do prompt**: `src/application/prompting/prompt_builder.py`
- **Caso de uso**: `src/application/use_cases/generate_report.py`
- **CLI**: `src/adapters/in_/cli/cli_controller.py`
- **Configuracao**: `config/config.json`

## Como rodar o projeto (exemplos)

Instalar deps:
```
pip install -r requirements.txt
```

Usando o CLI (main):
```
python main.py generate-report --source azure --id 359337 --report qa --ai gemini
```

Usando modulo direto:
```
python -m src.adapters.in_.cli.cli_controller generate-report --source azure --id 359337 --report risks --ai gemini
```

Rodar testes:
```
python -m pytest
```

## Testes

Unitarios:
- Parsing de campos do card
- Montagem de prompt
- Resolucao por registry

Integracao (com fakes/mocks):
- Fonte Azure/Jira simulada
- Cliente de IA simulado
- Execucao do caso de uso completo

Como executar:
```
python -m pytest
```

## Script legado (opcional)

O arquivo `conexao-azure-gemini-certo.py` foi mantido como referencia.  
Recomenda-se usar o CLI novo com variaveis de ambiente.

- Migrar o script atual para a estrutura proposta
- Extrair tokens para variaveis de ambiente
- Implementar CLI oficial (`main.py`)
- Criar registries e builders
