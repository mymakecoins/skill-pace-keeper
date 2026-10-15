#!/usr/bin/env python3
"""
test_export_html.py - Testes unitários para export_html.py do pace-keeper.
"""
import tempfile
import unittest
from pathlib import Path

from export_html import markdown_to_html, parse_inline_markdown, extract_metadata


class TestExportHtml(unittest.TestCase):

    def test_parse_inline_markdown(self):
        text = "Texto com **negrito**, *itálico*, `código` e [link](https://exemplo.com)"
        parsed = parse_inline_markdown(text)
        self.assertIn("<strong>negrito</strong>", parsed)
        self.assertIn("<em>itálico</em>", parsed)
        self.assertIn("<code>código</code>", parsed)
        self.assertIn('<a href="https://exemplo.com" target="_blank">link</a>', parsed)

    def test_extract_metadata(self):
        lines = [
            "# Relatório de Ritmo",
            "**Projeto Local:** meu-projeto",
            "**Repositório GitHub:** [org/repo](https://github.com/org/repo)",
            "**Milestone:** v1.0.0",
            "**Data Limite (Deadline):** 23/10/2026",
            "---",
            "## 1. Diagnóstico"
        ]
        meta, h1_title, remaining = extract_metadata(lines)
        self.assertEqual(h1_title, "Relatório de Ritmo")
        self.assertEqual(meta["projeto"], "meu-projeto")
        self.assertIn("org/repo", meta["repo"])
        self.assertEqual(meta["milestone"], "v1.0.0")
        self.assertEqual(meta["deadline"], "23/10/2026")
        self.assertEqual(remaining[0].strip(), "## 1. Diagnóstico")

    def test_markdown_to_html_full(self):
        md = """# Relatório de Ritmo e Capacidade de Entrega
**Projeto Local:** loggiq-main
**Milestone:** v1.0.0
**Data Limite (Deadline):** 23/10/2026

> [!IMPORTANT]
> Atualização de escopo importante realizada.

## 1. Diagnóstico da Janela Temporal
Tabela de parâmetros:

| Parâmetro | Valor | Detalhamento |
| :--- | :---: | :--- |
| **Dias Corridos** | 9 | Intervalo total |
| **Dias Úteis Líquidos** | 6.0 | Descontado buffer |

## 4. Gestão do Caminho Crítico
```mermaid
flowchart TD
    A[Início] --> B[Fim]
```

## 5. Cronograma Tático de Marcos
| Dia / Data | Foco Operacional | Issues Alocadas | Meta Diária |
| :--- | :--- | :--- | :---: |
| **Dia 1 (Qua) 14/10** | Liquidação | #101 > #102 > #103 | 3 cards |

## 6. Governança Estratégica
### 6.1 Pontos de Atenção para o Tech Leader
- Concorrência de banco no cadastro.

### 6.2 Pontos de Atenção para o Gerente de Projetos (GP)
- Margem de segurança de 1 dia preservada.

### 6.3 Notas para Outros Analistas
- N/A — Analista único atuando na esteira.
"""
        html_output = markdown_to_html(md)
        self.assertIn("<!DOCTYPE html>", html_output)
        self.assertIn("<style>", html_output)
        self.assertIn("meta-grid", html_output)
        self.assertIn("loggiq-main", html_output)
        self.assertIn("callout-success", html_output)
        self.assertIn("<table", html_output)
        self.assertIn("diagram-container", html_output)
        self.assertIn("class=\"mermaid\"", html_output)
        self.assertIn("#101 &gt; #102 &gt; #103", html_output)
        self.assertIn("Tech Leader", html_output)
        self.assertIn("Gerente de Projetos", html_output)
        self.assertIn("Outros Analistas", html_output)
        self.assertIn("mermaid.initialize", html_output)


if __name__ == "__main__":
    unittest.main()
