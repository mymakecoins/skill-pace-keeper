#!/usr/bin/env python3
"""
export_html.py
Converte o relatório markdown do Pace Keeper em um documento HTML 100% autônomo (standalone),
com CSS executivo embutido, suporte a tema escuro/claro, renderização adaptativa de Mermaid 10
e visual alinhado ao padrão oficial da skill.
Zero dependências externas (apenas biblioteca padrão Python).
"""
from __future__ import annotations

import argparse
import datetime
import html
import re
import sys
from pathlib import Path

EMBEDDED_CSS = """
:root {
  --bg-primary: #f8fafc;
  --bg-card: #ffffff;
  --text-main: #0f172a;
  --text-muted: #475569;
  --border-color: #e2e8f0;
  --brand-primary: #2563eb;
  --brand-dark: #1e40af;
  --brand-light: #eff6ff;
  --success-bg: #dcfce7;
  --success-text: #166534;
  --warning-bg: #fef9c3;
  --warning-text: #854d0e;
  --danger-bg: #fee2e2;
  --danger-text: #991b1b;
  --code-bg: #f1f5f9;
  --code-text: #0f172a;
  --badge-neutral-bg: #f1f5f9;
  --badge-neutral-text: #334155;
}

@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #0f172a;
    --bg-card: #1e293b;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --border-color: #334155;
    --brand-primary: #3b82f6;
    --brand-dark: #60a5fa;
    --brand-light: #1e3a8a33;
    --success-bg: #14532d44;
    --success-text: #4ade80;
    --warning-bg: #713f1244;
    --warning-text: #fde047;
    --danger-bg: #7f1d1d44;
    --danger-text: #f87171;
    --code-bg: #090d16;
    --code-text: #e2e8f0;
    --badge-neutral-bg: #334155;
    --badge-neutral-text: #cbd5e1;
  }
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.6;
  color: var(--text-main);
  background-color: var(--bg-primary);
  padding: 2.5rem 1rem;
}

.container {
  max-width: 1040px;
  margin: 0 auto;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 2.5rem 3rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
}

header {
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 1.5rem;
  margin-bottom: 2rem;
}

h1 {
  font-size: 1.85rem;
  font-weight: 700;
  color: var(--brand-dark);
  letter-spacing: -0.02em;
  margin-bottom: 0.75rem;
}

.subtitle {
  font-size: 1.05rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
}

.meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
  background: var(--brand-light);
  border: 1px solid var(--border-color);
  border-left: 4px solid var(--brand-primary);
  padding: 1.25rem;
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 0.925rem;
}

.meta-item strong {
  display: block;
  color: var(--text-muted);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.25rem;
}

.meta-item span, .meta-item a {
  color: var(--text-main);
  font-weight: 600;
  text-decoration: none;
}

.meta-item a:hover {
  text-decoration: underline;
  color: var(--brand-primary);
}

h2 {
  font-size: 1.35rem;
  font-weight: 700;
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-main);
  letter-spacing: -0.01em;
}

h3 {
  font-size: 1.15rem;
  font-weight: 600;
  margin-top: 1.75rem;
  margin-bottom: 0.75rem;
  color: var(--brand-primary);
}

h4 {
  font-size: 1rem;
  font-weight: 600;
  margin-top: 1.25rem;
  margin-bottom: 0.5rem;
  color: var(--text-main);
}

p {
  margin-bottom: 1rem;
  font-size: 0.975rem;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.25rem 0 2rem 0;
  font-size: 0.925rem;
}

th, td {
  padding: 0.85rem 1rem;
  border: 1px solid var(--border-color);
  text-align: left;
}

th {
  background-color: var(--code-bg);
  font-weight: 600;
  color: var(--text-main);
}

tr:nth-child(even) td {
  background-color: rgba(148, 163, 184, 0.04);
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 9999px;
  line-height: 1;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.badge-success { background: var(--success-bg); color: var(--success-text); }
.badge-warning { background: var(--warning-bg); color: var(--warning-text); }
.badge-danger { background: var(--danger-bg); color: var(--danger-text); }
.badge-neutral { background: var(--badge-neutral-bg); color: var(--badge-neutral-text); }
.badge-brand { background: var(--brand-light); color: var(--brand-primary); }

.callout {
  border-left: 4px solid var(--brand-primary);
  background-color: var(--code-bg);
  padding: 1rem 1.25rem;
  border-radius: 0 8px 8px 0;
  margin: 1.5rem 0;
  font-size: 0.925rem;
}

.callout-success {
  border-left-color: #10b981;
  background-color: var(--success-bg);
  color: var(--success-text);
}

.callout-warning {
  border-left-color: #eab308;
  background-color: var(--warning-bg);
  color: var(--warning-text);
}

.callout-danger {
  border-left-color: #ef4444;
  background-color: var(--danger-bg);
  color: var(--danger-text);
}

.metrics-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0 2rem 0;
}

.metric-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 1.25rem;
  border-radius: 8px;
  text-align: center;
}

.metric-card .value {
  font-size: 1.85rem;
  font-weight: 700;
  color: var(--brand-primary);
  line-height: 1.2;
  margin-bottom: 0.25rem;
}

.metric-card .label {
  font-size: 0.8rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
  font-weight: 600;
}

.diagram-container {
  background: var(--code-bg);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1.5rem 0;
  overflow-x: auto;
  text-align: center;
}

ul, ol {
  margin: 0.75rem 0 1.25rem 1.75rem;
  font-size: 0.95rem;
}

li {
  margin-bottom: 0.4rem;
}

li > ul, li > ol {
  margin-top: 0.3rem;
  margin-bottom: 0.5rem;
}

code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 0.875em;
  background-color: var(--code-bg);
  color: var(--code-text);
  padding: 0.15rem 0.4rem;
  border-radius: 4px;
  border: 1px solid var(--border-color);
}

pre {
  background-color: var(--code-bg);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  overflow-x: auto;
  margin: 1rem 0;
}

pre code {
  background: transparent;
  padding: 0;
  border: none;
}

hr {
  border: 0;
  height: 1px;
  background: var(--border-color);
  margin: 2.25rem 0;
}

footer {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
  font-size: 0.85rem;
  color: var(--text-muted);
  text-align: center;
}

@media print {
  body { padding: 0; background: #fff; color: #000; }
  .container { border: none; box-shadow: none; padding: 0; max-width: 100%; }
  .diagram-container { border: 1px solid #ccc; }
}
"""

MERMAID_SCRIPT = """
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({
    startOnLoad: true,
    theme: window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'neutral',
    flowchart: { useMaxWidth: true, htmlLabels: true, curve: 'basis' }
  });
</script>
"""


def parse_inline_markdown(text: str) -> str:
    """Aplica parsing inline: links, formatações, badges e código."""
    # Escapar caracteres HTML básicos
    text = html.escape(text, quote=False)

    # Badges automáticos comuns de complexidade e status
    def badge_replacer(match):
        raw = match.group(1).strip()
        val = raw.upper()
        if any(k in val for k in ["P (1 PT)", "P (1 PONTO)", "PESO 1", "P"]):
            return f'<span class="badge badge-neutral">{raw}</span>'
        if any(k in val for k in ["M (2 PTS)", "M (2 PONTOS)", "PESO 2", "M"]):
            return f'<span class="badge badge-warning">{raw}</span>'
        if any(k in val for k in ["G (4 PTS)", "G (4 PONTOS)", "PESO 4", "G", "BLOCKED", "BLOQUEADO"]):
            return f'<span class="badge badge-danger">{raw}</span>'
        if any(k in val for k in ["DONE", "CONCLUÍDO", "FINALIZADO", "LIBERADO", "RELEASE", "EM DIA"]):
            return f'<span class="badge badge-success">{raw}</span>'
        if any(k in val for k in ["CARDS", "PTS", "PONTOS", "V1.", "V2.", "V0."]):
            return f'<span class="badge badge-brand">{raw}</span>'
        return f'<span class="badge badge-neutral">{raw}</span>'

    text = re.sub(r'\[badge:([^\]]+)\]', badge_replacer, text, flags=re.IGNORECASE)

    # Código inline `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # Negrito **bold** ou __bold__
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', text)

    # Itálico *italic* ou _italic_
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'(?<=\s)_([^_]+)_(?=\s|[.,;:!?]|$)', r'<em>\1</em>', text)

    # Links [label](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', text)

    return text


def extract_metadata(lines: list[str]) -> tuple[dict[str, str], str, list[str]]:
    """Extrai campos de metadados do topo do markdown e retorna metadados + título h1 + linhas restantes."""
    meta: dict[str, str] = {}
    remaining_lines: list[str] = []
    in_meta_header = True
    h1_title = "Relatório de Ritmo e Capacidade de Entrega — Pace Keeper"

    # Padrões comuns de chaves de metadados
    meta_patterns = {
        "projeto": ["projeto local", "projeto", "nome do projeto"],
        "repo": ["repositório github", "repositório", "repositorio", "repo"],
        "board": ["github projects", "board", "quadro"],
        "milestone": ["milestone", "marco", "versão", "versao"],
        "data_analise": ["data da análise", "data da analise", "data da apuração", "data"],
        "deadline": ["data limite (deadline)", "data limite", "deadline", "prazo final"],
        "capacidade": ["capacidade técnica", "capacidade", "analistas", "equipe"],
        "criterio": ["critério de entrega", "criterio de entrega", "critério", "criterio"]
    }

    for line in lines:
        stripped = line.strip()
        if in_meta_header and stripped.startswith("# "):
            h1_title = stripped[2:].strip()
            continue

        if in_meta_header and stripped.startswith("---"):
            in_meta_header = False
            continue

        if in_meta_header and stripped.startswith("**"):
            # Linha de metadado ex: **Projeto Local:** loggiq-main
            match = re.match(r"^\*\*([^:]+):\*\*\s*(.*)$", stripped)
            if match:
                key = match.group(1).strip().lower()
                val = match.group(2).strip()
                matched_key = None
                for std_key, aliases in meta_patterns.items():
                    if key in aliases:
                        matched_key = std_key
                        break
                if matched_key:
                    meta[matched_key] = val
                    continue

        # Se chegamos a um subtítulo ## ou linha de conteúdo sem meta, finaliza bloco meta
        if stripped.startswith("## ") or stripped.startswith("> [!"):
            in_meta_header = False

        if not in_meta_header or not stripped.startswith("**"):
            remaining_lines.append(line)

    return meta, h1_title, remaining_lines


def build_meta_grid_html(meta: dict[str, str]) -> str:
    """Monta a grade de metadados visual (.meta-grid)."""
    if not meta:
        return ""

    labels = {
        "projeto": "Projeto Local",
        "repo": "Repositório GitHub",
        "board": "GitHub Projects",
        "milestone": "Milestone",
        "data_analise": "Data da Análise",
        "deadline": "Data Limite (Deadline)",
        "capacidade": "Capacidade Técnica",
        "criterio": "Critério de Entrega"
    }

    items_html = []
    for key, label in labels.items():
        if key in meta:
            raw_val = meta[key]
            # Formata badge se for milestone ou deadline
            parsed_val = parse_inline_markdown(raw_val)
            if key == "milestone" and not "<span class=" in parsed_val:
                parsed_val = f'<span class="badge badge-brand">{parsed_val}</span>'
            elif key == "deadline" and not "<span class=" in parsed_val:
                parsed_val = f'<span class="badge badge-warning">{parsed_val}</span>'

            items_html.append(f"""      <div class="meta-item">
        <strong>{label}</strong>
        <span>{parsed_val}</span>
      </div>""")

    if not items_html:
        return ""

    return '<div class="meta-grid">\n' + "\n".join(items_html) + "\n    </div>"


def markdown_to_html(md_content: str, title: str = "Relatório de Ritmo e Capacidade de Entrega — Pace Keeper") -> str:
    """Converte conteúdo Markdown estruturado em HTML autônomo com suporte a Mermaid, badges e tema."""
    raw_lines = md_content.splitlines()

    # Extrai metadados do cabeçalho
    meta, h1_title, lines = extract_metadata(raw_lines)
    if h1_title and title == "Relatório de Ritmo e Capacidade de Entrega — Pace Keeper":
        title = h1_title
    meta_grid_html = build_meta_grid_html(meta)

    # Constrói o cabeçalho executivo sempre
    header_html = f"""<header>
  <h1>{parse_inline_markdown(title)}</h1>
  <div class="subtitle">Auditoria determinística de backlog, capacidade líquida e caminho crítico — Skill Pace Keeper</div>
  {meta_grid_html}
</header>"""

    html_lines = [header_html]
    in_list = False
    in_sublist = False
    in_table = False
    in_blockquote = False
    in_mermaid = False
    mermaid_buffer = []

    i = 0
    n = len(lines)

    while i < n:
        raw_line = lines[i]
        line = raw_line.strip()

        # Blocos Mermaid
        if line.startswith("```mermaid"):
            in_mermaid = True
            mermaid_buffer = []
            i += 1
            continue

        if in_mermaid:
            if line.startswith("```"):
                in_mermaid = False
                diagram_code = "\n".join(mermaid_buffer)
                html_lines.append(f"""<div class="diagram-container">
  <div class="mermaid">
{diagram_code}
  </div>
</div>""")
            else:
                mermaid_buffer.append(raw_line)
            i += 1
            continue

        # Fechar listas se a linha atual não for item de lista
        is_list_item = line.startswith(("- ", "* ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ")) or (raw_line.startswith("  - ") or raw_line.startswith("    - "))
        if not is_list_item:
            if in_sublist:
                html_lines.append("</ul>")
                in_sublist = False
            if in_list:
                html_lines.append("</ul>")
                in_list = False

        # Fechar blockquote se linha não for citação
        if in_blockquote and not line.startswith(">"):
            html_lines.append("</div>")
            in_blockquote = False

        # Fechar tabela se linha não for tabela
        if in_table and not line.startswith("|"):
            html_lines.append("</tbody>\n</table>")
            in_table = False

        # Linha em branco
        if not line:
            i += 1
            continue

        # Headings secundários
        if line.startswith("# "):
            # H1 adicional no corpo
            h1_text = parse_inline_markdown(line[2:].strip())
            html_lines.append(f"<h2>{h1_text}</h2>")
            i += 1
            continue

        if line.startswith("## "):
            h2_text = parse_inline_markdown(line[3:].strip())
            html_lines.append(f"\n<section>\n  <h2>{h2_text}</h2>")
            i += 1
            continue

        if line.startswith("### "):
            h3_text = parse_inline_markdown(line[4:].strip())
            html_lines.append(f"  <h3>{h3_text}</h3>")
            i += 1
            continue

        if line.startswith("#### "):
            h4_text = parse_inline_markdown(line[5:].strip())
            html_lines.append(f"  <h4>{h4_text}</h4>")
            i += 1
            continue

        # Horizontal Rule
        if line in ("---", "***", "___"):
            html_lines.append("</section>")
            html_lines.append("<hr>")
            i += 1
            continue

        # Callouts e Blockquotes
        if line.startswith(">"):
            quote_text = line[1:].strip()
            # Detectar tipos de alerta GitHub
            callout_class = "callout"
            if quote_text.startswith("[!IMPORTANT]") or quote_text.startswith("[!NOTE]"):
                callout_class = "callout callout-success"
                quote_text = re.sub(r"^\[!(?:IMPORTANT|NOTE)\]\s*", "", quote_text)
            elif quote_text.startswith("[!WARNING]"):
                callout_class = "callout callout-warning"
                quote_text = re.sub(r"^\[!WARNING\]\s*", "", quote_text)
            elif quote_text.startswith("[!CAUTION]") or quote_text.startswith("[!DANGER]"):
                callout_class = "callout callout-danger"
                quote_text = re.sub(r"^\[!(?:CAUTION|DANGER)\]\s*", "", quote_text)
            elif "alerta" in quote_text.lower() or "atenção" in quote_text.lower() or "atencao" in quote_text.lower():
                callout_class = "callout callout-warning"
            elif "sucesso" in quote_text.lower() or "atualização" in quote_text.lower() or "desescopo" in quote_text.lower():
                callout_class = "callout callout-success"

            parsed_quote = parse_inline_markdown(quote_text)
            if not in_blockquote:
                html_lines.append(f'<div class="{callout_class}">')
                in_blockquote = True
            html_lines.append(f"  <p>{parsed_quote}</p>")
            i += 1
            continue

        # Tabelas
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            # Se for linha de separador/alinhamento | :--- | :---: |
            if re.match(r"^\|(?:\s*:?-+:?\s*\|)+$", line):
                i += 1
                continue

            if not in_table:
                # Linha de cabeçalho da tabela
                th_elements = "".join([f"<th>{parse_inline_markdown(c)}</th>" for c in cells])
                html_lines.append(f'<table>\n  <thead>\n    <tr>{th_elements}</tr>\n  </thead>\n  <tbody>')
                in_table = True
                i += 1
                continue
            else:
                # Linha de dados
                td_elements = []
                for idx, c in enumerate(cells):
                    parsed_cell = parse_inline_markdown(c)
                    # Formatar sequência de issues com estilo
                    if "#" in parsed_cell and "&gt;" in parsed_cell:
                        # Ex: #101 &gt; #102
                        pass
                    # Formatar alinhamento se for numérico ou central
                    if any(c.strip().startswith(prefix) for prefix in ["Dia ", "Fim de Semana", "Total"]):
                        td_elements.append(f"<td><strong>{parsed_cell}</strong></td>")
                    elif re.match(r"^(\d+[\d,.]*|\d+\s*(cards|pts|subtarefas)|[0-9/]+)$", c.strip(), re.IGNORECASE):
                        td_elements.append(f'<td style="text-align: center;">{parsed_cell}</td>')
                    else:
                        td_elements.append(f"<td>{parsed_cell}</td>")

                html_lines.append(f'    <tr>{"".join(td_elements)}</tr>')
                i += 1
                continue

        # Listas
        if is_list_item:
            item_text = re.sub(r"^(?:[-*]|\d+\.)\s+", "", line)
            parsed_item = parse_inline_markdown(item_text)
            if raw_line.startswith(("  - ", "  * ", "    - ", "\t- ")):
                if not in_sublist:
                    html_lines.append("<ul>")
                    in_sublist = True
                html_lines.append(f"  <li>{parsed_item}</li>")
            else:
                if in_sublist:
                    html_lines.append("</ul>")
                    in_sublist = False
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                html_lines.append(f"<li>{parsed_item}</li>")
            i += 1
            continue

        # Parágrafo normal
        parsed_p = parse_inline_markdown(line)
        html_lines.append(f"<p>{parsed_p}</p>")
        i += 1

    # Fechamentos residuais
    if in_sublist:
        html_lines.append("</ul>")
    if in_list:
        html_lines.append("</ul>")
    if in_table:
        html_lines.append("</tbody>\n</table>")
    if in_blockquote:
        html_lines.append("</div>")

    body_html = "\n".join(html_lines)
    # Garante fechamento de seções abertas se houver
    if "<section>" in body_html:
        body_html += "\n</section>"

    now_str = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M")
    footer_html = f"""  <footer>
    Relatório gerado via Pace Keeper em {now_str} • Formato Standalone com CSS Embutido
  </footer>"""

    complete_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <style>
{EMBEDDED_CSS}
  </style>
</head>
<body>

<div class="container">
{body_html}
{footer_html}
</div>

{MERMAID_SCRIPT}
</body>
</html>
"""
    return complete_html


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converte relatório do Pace Keeper (.md) para HTML standalone com CSS embutido e Mermaid."
    )
    parser.add_argument("markdown_file", type=Path, help="Caminho do arquivo Markdown gerado pelo Pace Keeper.")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Caminho do arquivo HTML de saída (padrão: mesmo nome com extensão .html)."
    )

    args = parser.parse_args()
    md_path: Path = args.markdown_file.resolve()

    if not md_path.is_file():
        print(f"Erro: Arquivo '{md_path}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    out_path = args.output.resolve() if args.output else md_path.with_suffix(".html")
    content = md_path.read_text(encoding="utf-8")

    title_match = re.search(r"^#\s+(.+)$", content, re.M)
    title = title_match.group(1).strip() if title_match else "Relatório de Ritmo — Pace Keeper"

    html_result = markdown_to_html(content, title=title)
    out_path.write_text(html_result, encoding="utf-8")

    print(f"Sucesso: Relatório HTML standalone gerado em: {out_path}")


if __name__ == "__main__":
    main()
