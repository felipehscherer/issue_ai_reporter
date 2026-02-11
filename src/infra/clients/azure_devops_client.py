import os
from typing import Any, Dict

import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.retry import Retry


class AzureDevOpsClient:
    def __init__(self, config: Dict[str, Any]) -> None:
        # Opcional: para Azure DevOps Server/URLs customizadas.
        # Exemplos:
        # - https://dev.azure.com/<org>
        # - https://<org>.visualstudio.com
        self._org_url = (config.get("org_url") or os.getenv("AZURE_DEVOPS_ORG_URL") or "").strip()
        self._organization = config.get("organization") or os.getenv("AZURE_DEVOPS_ORG")
        self._project = config.get("project") or os.getenv("AZURE_DEVOPS_PROJECT")
        self._pat = config.get("pat") or os.getenv("AZURE_DEVOPS_PAT")
        if (not self._org_url and not self._organization) or not self._project or not self._pat:
            raise ValueError(
                "AZURE_DEVOPS_PROJECT e AZURE_DEVOPS_PAT sao obrigatorios, e voce deve definir "
                "AZURE_DEVOPS_ORG (nome da org) ou AZURE_DEVOPS_ORG_URL (URL completa da org)."
            )

        # Session com retry para instabilidades de rede (ex: reset de conexao).
        self._session = requests.Session()
        retry = Retry(
            total=4,
            connect=4,
            read=4,
            backoff_factor=0.6,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET"]),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def get_work_item(self, work_item_id: str) -> Dict[str, Any]:
        base = self._org_url.rstrip("/") if self._org_url else f"https://dev.azure.com/{self._organization}"
        url = f"{base}/{self._project}/_apis/wit/workitems/{work_item_id}?api-version=7.0"

        try:
            response = self._session.get(
                url,
                auth=HTTPBasicAuth("", self._pat),
                headers={
                    "Accept": "application/json",
                    "User-Agent": "issue-ai-reporter/1.0",
                },
                timeout=30,
            )
        except requests.exceptions.Timeout as e:
            raise RuntimeError(
                "Timeout ao consultar Azure DevOps. Possiveis causas: VPN/proxy, instabilidade de rede, "
                "ou endpoint incorreto. Verifique acesso ao Azure no navegador e tente novamente."
            ) from e
        except requests.exceptions.SSLError as e:
            raise RuntimeError(
                "Falha SSL/TLS ao conectar no Azure DevOps. Em redes corporativas, isso costuma ser proxy/inspecao "
                "SSL sem certificado confiavel. Tente configurar REQUESTS_CA_BUNDLE/SSL_CERT_FILE, ou usar a VPN/proxy "
                "corretos. Se sua org usa URL diferente, defina AZURE_DEVOPS_ORG_URL."
            ) from e
        except requests.exceptions.ProxyError as e:
            raise RuntimeError(
                "Erro de proxy ao conectar no Azure DevOps. Verifique HTTPS_PROXY/HTTP_PROXY (ou a configuracao do proxy "
                "do sistema) e tente novamente."
            ) from e
        except requests.exceptions.ConnectionError as e:
            raise RuntimeError(
                "Conexao abortada ao conectar no Azure DevOps (ex: WinError 10054). Isso normalmente indica bloqueio/queda "
                "de rede (firewall, proxy, VPN) ou endpoint incorreto. Verifique se consegue abrir o Azure no navegador, "
                "tente outra rede/VPN e, se necessario, defina AZURE_DEVOPS_ORG_URL."
            ) from e
        except requests.exceptions.RequestException as e:
            raise RuntimeError("Erro de rede ao consultar Azure DevOps.") from e

        if response.status_code != 200:
            raise RuntimeError(f"Erro no Azure: {response.status_code} - {response.text}")
        return response.json()
