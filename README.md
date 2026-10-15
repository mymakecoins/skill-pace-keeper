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

## 📄 Licença

Distribuído sob a licença MIT. Consulte o repositório para mais informações.
