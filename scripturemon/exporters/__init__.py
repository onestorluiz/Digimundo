"""
EXPORTERS: Result Formatters

Exportacao de resultados da analise Triple-Core.

Formatos:
- TXT: 5 fases humanizadas em portugues
- HTML: 4 partes coloridas com navegacao

Exporter principal: FormattedExporter
- export_txt(): Gera .txt humanizado
- export_html(): Gera .html estruturado

Output location: workspace/outputs/formatted/
"""

__exporters__ = ["FormattedExporter"]

from triple_core.exporters.formatted_exporter import FormattedExporter

__all__ = ["FormattedExporter"]
