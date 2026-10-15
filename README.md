# Pace Keeper — Guardião de Ritmo, Capacidade e Prazos de Entrega

[![Skill](https://img.shields.io/badge/Antigravity-Skill-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

O **Pace Keeper** é uma skill para assistentes de IA (Google Antigravity / Claude / agentes autônomos) especializada em calcular a velocidade de desenvolvimento necessária, capacidade diária, caminho crítico e cadência de entrega para cumprir prazos rígidos (*deadlines*) em projetos de software orientados a especificações (SDD, Spec Kit, GitHub Projects ou backlogs em Markdown).

---

## 🎯 Objetivo

Converter prazos de entrega fixos e escopos de software em métricas práticas, factíveis e auditáveis:
- **Throughput Diário Necessário:** Quantidade de tarefas macro, subtarefas atômicas e pontos de esforço por dia útil líquido e dia corrido (total da equipe e *per capita* por analista).
- **Segregação Rigorosa de Entregas:** Separação entre issues macro (histórias/cards de negócio) e sub-issues/subtarefas atômicas técnicas.
- **Mapeamento do Caminho Crítico:** Identificação de itens gargalo (complexidade G), dependências técnicas e datas limite de corte (*drop-dead dates*).
- **Cronograma Tático com Ordem Sequencial:** Alocação diária de tarefas com notação sequencial de dependência (`#101 > #102 > #103`).
- **Tríade de Governança Estratégica:** Recomendações e alertas focados para o **Tech Leader**, **Gerente de Projetos (GP/PM)** e **Outros Analistas**.
- **Entrega Dupla Automatizada:** Exibição do relatório em Markdown no chat e geração automática em disco da versão **Markdown** e da versão **HTML Standalone Executiva** com CSS embutido.

---

## 🧠 Destaques e Diferenciais

1. **Sem Suposições ou Alucinações:** Análise fundamentada em evidências factuais do repositório, branches, commits e quadros do GitHub.
2. **Buffer Obrigatório de Homologação:** Reserva determinística de 1,0 a 1,5 dias úteis finais para *Code Freeze*, testes de integração e estabilização de staging.
3. **Qualidade Inviolável:** Aumento de ritmo não autoriza corte de testes unitários ou acúmulo irresponsável de débitos técnicos.
4. **HTML Standalone Executivo:** Visual profissional com suporte a tema claro/escuro (`prefers-color-scheme`), diagramas Mermaid interativos, cards de métricas e badges semânticos, sem dependências externas de compilação.

---

## 📂 Estrutura do Repositório

```text
.
├── SKILL.md                          # Instruções formais, regras de sondagem e metodologia
├── README.md                         # Documentação do repositório
├── .gitignore                        # Regras de exclusão de artefatos temporários
├── scripts/
│   ├── calculate_pace.py             # Script utilitário para cálculo de capacidade e throughput
│   ├── export_html.py                # Compilador de Markdown para HTML Standalone com CSS embutido
│   └── test_export_html.py           # Suíte de testes unitários do exportador HTML
└── templates/
    └── pace-keeper-template.html     # Template base com CSS executivo, temas e suporte Mermaid
```

---

## 🚀 Como Usar os Scripts Auxiliares

### 1. Cálculo de Ritmo e Capacidade (`calculate_pace.py`)

Calcula dias corridos, dias úteis líquidos (descontando feriados e buffer) e velocidades requeridas:

```bash
python3 scripts/calculate_pace.py \
  --start-date 2026-10-15 \
  --target-date 2026-10-23 \
  --tasks-p 8 \
  --tasks-m 6 \
  --tasks-g 2 \
  --atomic-tasks 45 \
  --analysts 2 \
  --buffer-days 1.0
```

#### Parâmetros:
- `--start-date`: Data de início do período (formato `AAAA-MM-DD`). Padrão: data de hoje.
- `--target-date`: Data limite (*deadline*) da entrega (obrigatório).
- `--tasks-p`: Quantidade de tarefas pequenas (peso 1 ponto).
- `--tasks-m`: Quantidade de tarefas médias (peso 2 pontos).
- `--tasks-g`: Quantidade de tarefas grandes/críticas (peso 4 pontos).
- `--atomic-tasks`: Total de subtarefas atômicas ou checklists pendentes.
- `--analysts`: Quantidade de analistas ativos no projeto (padrão: 1).
- `--buffer-days`: Dias reservados para *Code Freeze* / Homologação (padrão: 1.0 dia).

---

### 2. Compilação do Relatório HTML Standalone (`export_html.py`)

Converte um arquivo Markdown gerado pelo Pace Keeper em uma página HTML autônoma e executiva:

```bash
python3 scripts/export_html.py "20261015-pace-keeper-meuprojeto-v1.0.0.md"
```

O script criará automaticamente `20261015-pace-keeper-meuprojeto-v1.0.0.html` no mesmo diretório, contendo:
- Metagrid executivo com metadados do projeto.
- Cards numéricos de resumo de capacidade e pendências.
- Tabelas executivas com alternância de linhas e badges de status.
- Diagrama de caminho crítico renderizado com Mermaid.js via CDN.
- Estilos responsivos otimizados para apresentação e compartilhamento com stakeholders.

---

### 3. Execução dos Testes Unitários (`test_export_html.py`)

Execute os testes unitários com o framework padrão do Python:

```bash
python3 -m unittest discover -s scripts
```

---

## 📋 Modos de Operação da Skill

| Modo | Cenário de Uso | Fonte de Dados |
| :--- | :--- | :--- |
| **Modo A** | Projetos gerenciados no GitHub | `gh project item-list` e `gh issue list --milestone` |
| **Modo B** | Especificações locais (Spec Kit / SDD) | Arquivos Markdown (`docs/tasks/`, `tasks.md`, `specs/`) |
| **Modo C** | Entrada paramétrica direta | Fornecimento direto de quantidades e complexidades no chat |

---

## 📊 Estrutura Padrão do Relatório de Ritmo

Todo relatório gerado pela skill segue 6 seções obrigatórias:

1. **Diagnóstico da Janela Temporal e Capacidade Real:** Datas, dias corridos, dias úteis de calendário, feriados, buffer e dias úteis líquidos.
2. **Estado do Backlog e Totalizadores de Entregas:** Totalizadores segregados (Issues Principais vs Subtarefas Atômicas) e distribuição por colunas do board.
3. **Velocidade Necessária (Throughput Diário):** Cards/dia, pontos/dia e subtarefas/dia (total e per capita).
4. **Gestão do Caminho Crítico e Gargalos:** Diagrama Mermaid de precedência e tabela de riscos de complexidade G com *Drop-Dead Dates*.
5. **Cronograma Tático de Marcos:** Alocação dia a dia no formato estrito `"Dia X (DiaSemana) DD/MM"` com sequência de execução (`#101 > #102 > #103`).
6. **Governança Estratégica e Alinhamentos:**
   - 🧠 *6.1 Pontos de Atenção para o Tech Leader*
   - 📈 *6.2 Pontos de Atenção para o GP / PM*
   - 👥 *6.3 Notas para Outros Analistas*

---

## 🛠️ Instalação no Ecossistema Antigravity

Clone ou adicione este repositório no diretório de skills personalizadas do Antigravity:

```bash
git clone git@github.com:mymakecoins/skill-pace-keeper.git ~/.gemini/config/skills/pace-keeper
```

A skill estará imediatamente disponível para invocação em sessões de pair-programming e auditorias de entrega.

---

## 🤖 Instalação e Uso no Ecossistema Claude

O **Pace Keeper** é totalmente compatível com o ecossistema Claude (Claude Code, Claude Projects e Claude Desktop).

### 1. Claude Code (CLI)

#### Opção A: Como Slash Command Global (`/pace-keeper`)
Vincule o arquivo `SKILL.md` ao diretório de comandos personalizados do Claude Code:

```bash
mkdir -p ~/.claude/commands
ln -sf /home/mmc/00_code/00_tools/_skills/pace-keeper/SKILL.md ~/.claude/commands/pace-keeper.md
```

> **Uso:** Em qualquer repositório, basta digitar `/pace-keeper` na sessão do Claude Code para acionar a sondagem inicial e a metodologia completa.

#### Opção B: Como Slash Command no Projeto Local
Se desejar disponibilizar a skill apenas em um repositório específico da equipe:

```bash
mkdir -p .claude/commands
cp /caminho/para/skill-pace-keeper/SKILL.md .claude/commands/pace-keeper.md
```

#### Opção C: Execução Automatizada via Bash
Como o Claude Code possui execução de comandos terminal via ferramenta bash, ele pode rodar diretamente os scripts oficiais da skill durante a sessão:

```bash
# Cálculo do throughput e capacidade
python3 /home/mmc/00_code/00_tools/_skills/pace-keeper/scripts/calculate_pace.py --target-date AAAA-MM-DD ...

# Compilação automática do relatório em HTML Standalone
python3 /home/mmc/00_code/00_tools/_skills/pace-keeper/scripts/export_html.py "AAAAMMDD-pace-keeper-projeto.md"
```

---

### 2. Claude Projects (claude.ai)

1. Crie ou acesse seu projeto no **Claude Projects**.
2. Cole o conteúdo de [`SKILL.md`](./SKILL.md) no campo **Project Instructions** (Instruções do Projeto).
3. Em **Project Knowledge** (Arquivos de Conhecimento), adicione os arquivos:
   - `templates/pace-keeper-template.html` (para renderização visual de referência).
   - `scripts/calculate_pace.py` e `scripts/export_html.py` (para referência algorítmica).
4. O Claude atuará automaticamente como o guardião de ritmo em todas as conversas dentro do projeto.

---

### 3. Claude Desktop / Prompt de Sistema

Adicione o conteúdo de [`SKILL.md`](./SKILL.md) como prompt de sistema ou instrução inicial ao iniciar planejamentos de sprint, revisões de milestone ou auditorias de entrega.

---

## ⚡ Instalação e Uso no Ecossistema Codex

O **Pace Keeper** é nativamente compatível com o ecossistema Codex (OpenAI Codex / Codex CLI / Agentes Codex), integrando-se diretamente ao catálogo de skills do ambiente.

### 1. Instalação Global no Diretório de Skills do Codex

Clone ou crie um link simbólico no diretório global de skills do Codex (`~/.codex/skills/`):

```bash
# Opção A: Clonagem direta
git clone git@github.com:mymakecoins/skill-pace-keeper.git ~/.codex/skills/pace-keeper

# Opção B: Link simbólico para repositório já clonado
ln -sf /home/mmc/00_code/00_tools/_skills/pace-keeper ~/.codex/skills/pace-keeper
```

Como o arquivo [`SKILL.md`](./SKILL.md) já possui o frontmatter YAML padrão (`name: pace-keeper`), o motor de agentes do Codex indexa a skill automaticamente ao iniciar novas sessões.

---

### 2. Integração por Projeto via `.codexrules`

Para instruir o agente Codex a adotar a disciplina de ritmo em um repositório específico, adicione ao seu arquivo `.codexrules` na raiz do projeto:

```markdown
## Governança de Ritmo e Prazos (Pace Keeper)
- Para estimativas de entrega, auditoria de backlog ou cálculo de viabilidade de milestones, execute a metodologia da skill `pace-keeper`.
- Reserve sempre o buffer obrigatório de homologação/staging (Code Freeze).
- Para persistir o diagnóstico, gere a entrega dupla (Markdown e HTML Standalone executivo via script):
  `python3 ~/.codex/skills/pace-keeper/scripts/export_html.py "AAAAMMDD-pace-keeper-<projeto>.md"`
```

---

### 3. Chamada Direta via CLI / Scripts no Codex

O agente Codex ou seus scripts de esteira podem invocar diretamente as ferramentas determinísticas:

```bash
# Calcular throughput e capacidade necessária
python3 ~/.codex/skills/pace-keeper/scripts/calculate_pace.py \
  --start-date AAAA-MM-DD \
  --target-date AAAA-MM-DD \
  --tasks-p 5 --tasks-m 8 --tasks-g 2 \
  --atomic-tasks 40 \
  --analysts 2

# Exportar relatório para HTML executivo com tema escuro/claro e Mermaid
python3 ~/.codex/skills/pace-keeper/scripts/export_html.py "AAAAMMDD-pace-keeper-projeto.md"
```

---

## 📄 Licença

Distribuído sob a licença MIT. Consulte o repositório para mais informações.
