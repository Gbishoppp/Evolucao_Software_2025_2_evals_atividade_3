# Atividade 3 - Praticas de Integracao Continua e Entrega Continua na Gerencia de Mudancas

## Informacoes da Equipe

**Disciplina:** Evolucao de Software 2025.2  
**Professor:** Glauco de Figueiredo Carneiro  
**Data de Entrega:** 29/01/2026

### Componentes da Equipe

| Nome                       | Matricula    |
| -------------------------- | ------------ |
| Gabriel Bispo Santana      | 202000012702 |
| Pedro Savio Souza da Silva | 202100114142 |
| Thiago Freire de Carvalho  | 202000013147 |
| Davi Santos Freire         | 201700053088 |

---

## 1. Projeto Selecionado

**Repositorio:** OpenAI Evals  
**URL:** https://github.com/openai/evals  
**Descricao:** Framework para avaliacao de LLMs (Large Language Models) e sistemas baseados em LLM, com um registro open-source de benchmarks.

### Informacoes Gerais do Projeto

| Metrica               | Valor          |
| --------------------- | -------------- |
| Linguagem Principal   | Python (89.4%) |
| Stars                 | 17.6k          |
| Forks                 | 2.9k           |
| Contributors          | 460+           |
| Commits               | 689            |
| Issues Abertas        | 113            |
| Pull Requests Abertos | 51             |
| Versao Atual          | 3.0.1.post1    |

---

## 2. Enquadramento: Cenario A - Projeto JA IMPLEMENTA CI/CD

O projeto OpenAI Evals **implementa CI/CD** atraves do GitHub Actions. O repositorio possui arquivos de workflow `.yml`, executa testes automaticos e possui ferramentas de linting via pre-commit hooks.

### Papel da Equipe: Auditores de Processo

---

## 3. Mapeamento das Ferramentas e Configuracoes

### 3.1 Ferramentas Utilizadas

| Ferramenta         | Finalidade                        | Arquivo de Configuracao    |
| ------------------ | --------------------------------- | -------------------------- |
| **GitHub Actions** | CI/CD Pipeline                    | `.github/workflows/*.yaml` |
| **pytest**         | Testes Unitarios                  | Executado via workflow     |
| **pre-commit**     | Hooks de Pre-commit               | `.pre-commit-config.yaml`  |
| **mypy**           | Verificacao de Tipos              | `mypy.ini`                 |
| **black**          | Formatacao de Codigo              | `.pre-commit-config.yaml`  |
| **isort**          | Ordenacao de Imports              | `.pre-commit-config.yaml`  |
| **autoflake**      | Remocao de Imports Nao Utilizados | `.pre-commit-config.yaml`  |
| **ruff**           | Linter Rapido                     | `.pre-commit-config.yaml`  |
| **Git LFS**        | Armazenamento de Arquivos Grandes | `.gitattributes`           |

### 3.2 Arquivos de Workflow do GitHub Actions

#### 3.2.1 `run_tests.yaml` - Testes Unitarios

**Localizacao:** `.github/workflows/run_tests.yaml`  
**URL:** https://github.com/openai/evals/blob/main/.github/workflows/run_tests.yaml

```yaml
name: Run unit tests

on:
  pull_request:
    branches:
      - main
  push:
    branches:
      - main

jobs:
  check_files:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
        with:
          fetch-depth: 0
          lfs: true

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyyaml
          pip install pytest
          pip install -e .[torch]

      - name: Run unit tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          pytest
```

**Gatilhos:**

- Pull Requests para branch `main`
- Push para branch `main`

#### 3.2.2 `test_eval.yaml` - Teste de Novos Evals

**Localizacao:** `.github/workflows/test_eval.yaml`  
**URL:** https://github.com/openai/evals/blob/main/.github/workflows/test_eval.yaml

```yaml
name: Run new evals

on:
  workflow_dispatch:
  pull_request:
    branches:
      - main
    paths:
      - "evals/registry/**"

jobs:
  check_files:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
        with:
          fetch-depth: 0
          lfs: true

      - name: Install Git LFS
        run: |
          sudo apt-get install git-lfs
          git lfs install

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyyaml
          pip install -e .

      - name: Get list of new YAML files in evals/registry/evals
        id: get_files
        run: |
          git diff --name-only --diff-filter=A ${{ github.event.pull_request.base.sha }} ${{ github.sha }} | grep '^evals/registry/evals/.*\.yaml$' | xargs > new_files
          echo "new_files=$(cat new_files)" >> $GITHUB_ENV

      - name: Run oaieval command for each new YAML file
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          files="${{ env.new_files }}"
          if [ -n "$files" ]; then
            for file in $files; do
              echo "Processing $file"
              first_key=$(python .github/workflows/parse_yaml.py $file)
              echo "Eval Name: $first_key"
              oaieval dummy $first_key --max_samples 10
            done
          else
            echo "No new YAML files found in evals/registry/evals"
          fi
```

**Gatilhos:**

- Disparo manual (`workflow_dispatch`)
- Pull Requests com alteracoes em `evals/registry/**`

### 3.3 Configuracao de Pre-commit Hooks

**Localizacao:** `.pre-commit-config.yaml`  
**URL:** https://github.com/openai/evals/blob/main/.pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: "v1.3.0"
    hooks:
      - id: mypy
        args: ["--config-file=mypy.ini", "--no-site-packages"]

  - repo: https://github.com/psf/black
    rev: 22.8.0
    hooks:
      - id: black
        args: [--line-length=100, --exclude=""]

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--line-length=100, --profile=black]

  - repo: https://github.com/PyCQA/autoflake
    rev: v1.6.1
    hooks:
      - id: autoflake
        args:
          - "--in-place"
          - "--expand-star-imports"
          - "--remove-duplicate-keys"
          - "--remove-unused-variables"
          - "--remove-all-unused-imports"
        exclude: "evals/__init__.py"

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.0.277
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix, --line-length=767]
```

---

## 4. Fluxograma do Pipeline Atual

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PIPELINE CI/CD - OpenAI Evals                        │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │   Developer  │
                              │   faz Push   │
                              └──────┬───────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │   Gatilho Acionado    │
                         │  (push ou PR p/ main) │
                         └───────────┬───────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   Pre-commit    │    │   Run Unit      │    │   Run New       │
    │   Hooks Local   │    │   Tests         │    │   Evals         │
    │                 │    │   (run_tests)   │    │   (test_eval)   │
    └────────┬────────┘    └────────┬────────┘    └────────┬────────┘
             │                      │                      │
             ▼                      ▼                      │
    ┌─────────────────┐    ┌─────────────────┐             │
    │ - mypy          │    │ 1. Checkout     │             │
    │ - black         │    │ 2. Setup Python │             │
    │ - isort         │    │    3.9          │             │
    │ - autoflake     │    │ 3. Install Deps │             │
    │ - ruff          │    │ 4. Run pytest   │             │
    └─────────────────┘    └────────┬────────┘             │
                                    │                      │
                                    ▼                      ▼
                           ┌─────────────────┐    ┌─────────────────┐
                           │   Testes        │    │ Testa novos     │
                           │   Unitarios     │    │ arquivos YAML   │
                           │   Executados    │    │ em registry/    │
                           └────────┬────────┘    └────────┬────────┘
                                    │                      │
                                    └──────────┬───────────┘
                                               │
                                               ▼
                                    ┌─────────────────────┐
                                    │   Resultado do CI   │
                                    │   (Pass/Fail)       │
                                    └─────────────────────┘
                                               │
                          ┌────────────────────┼────────────────────┐
                          │                    │                    │
                          ▼                    ▼                    ▼
                   ┌────────────┐       ┌────────────┐       ┌────────────┐
                   │   SUCESSO  │       │   FALHA    │       │  PENDENTE  │
                   │   (verde)  │       │  (vermelho)│       │ (amarelo)  │
                   └────────────┘       └────────────┘       └────────────┘
```

---

## 5. Analise de Eficiencia do CI/CD

### 5.1 Tempo de Feedback

| Workflow       | Tempo Medio  | Observacoes                    |
| -------------- | ------------ | ------------------------------ |
| Run unit tests | 3-12 minutos | Varia conforme dependencias    |
| Run new evals  | ~10 minutos  | Depende da quantidade de evals |

**Analise:** O tempo de feedback e **razoavel** para um projeto desta escala. Com tempos entre 3-12 minutos, os desenvolvedores recebem retorno relativamente rapido sobre a qualidade de suas contribuicoes.

**Evidencias de Execucao:**

- Run #1788 (push main): 3m 41s
- Run #1807 (PR #1605): 12m 1s
- Run #2295 (new evals): 10m 18s

### 5.2 Confiabilidade dos Testes

**Observacoes:**

- O ultimo workflow executado no branch `main` (Run #1808) **falhou** apos o merge do PR #1605
- PRs de contribuidores externos frequentemente ficam com status "action_required" aguardando aprovacao para executar workflows

**Problemas Identificados:**

1. **Testes instáveis em PRs externos:** PRs de forks requerem aprovacao manual para executar workflows (seguranca do GitHub)
2. **Falhas pos-merge:** Evidencia de que codigo pode ser mergeado mesmo com testes falhando posteriormente

### 5.3 Bloqueio de Regressao

**Configuracao Atual:**

- O CI **executa** em todos os PRs para main
- **NAO ha branch protection rules** visiveis que bloqueiem merge automaticamente
- PRs de membros da organizacao (como `maxb-openai`) podem ser mergeados sem aguardar CI

**Evidencia de PR Bloqueado:**

- PR #1607 (Update to Python 3.12) esta aberto desde 21/12/2025 com status "Action required"
- Isso indica que PRs de contribuidores externos sao **bloqueados** ate aprovacao manual

**Lacuna Identificada:**
O PR #1605 foi mergeado e o workflow subsequente no main **falhou**, indicando que:

- O merge foi realizado antes da conclusao bem-sucedida do CI
- Ou houve falha apos o merge devido a condicoes do ambiente

---

## 6. Analise Unificada: Impacto na Evolucao

### 6.1 Refatoracao e Divida Tecnica

**Impacto da Presenca de CI/CD:**

| Aspecto              | Situacao Atual                          | Impacto                                          |
| -------------------- | --------------------------------------- | ------------------------------------------------ |
| Pre-commit hooks     | Configurados (mypy, black, isort, ruff) | **Positivo** - Codigo formatado consistentemente |
| Testes unitarios     | Executados automaticamente              | **Positivo** - Detecta regressoes basicas        |
| Cobertura de testes  | Nao visivel/configurada                 | **Negativo** - Dificil medir qualidade           |
| Verificacao de tipos | mypy configurado                        | **Positivo** - Reduz bugs de tipo                |

**Coragem para Refatoracao:**

- A presenca de testes automaticos **aumenta moderadamente** a confianca dos desenvolvedores
- **Limitacao:** Sem metricas de cobertura de codigo, refatoracoes grandes ainda carregam riscos
- O fato de PRs poderem ser mergeados com CI falhando **reduz** a confianca no pipeline

### 6.2 Frequencia de Releases

**Historico de Tags/Releases:**

| Versao | Data Aproximada | Intervalo |
| ------ | --------------- | --------- |
| v0.1.1 | Janeiro 2023    | -         |
| 1.0.1  | 2023            | ~6 meses  |
| 1.0.2  | 2023            | ~2 meses  |
| 1.0.3  | 2023            | ~2 meses  |
| 2.0.0  | 2024            | ~6 meses  |
| 3.0.0  | Abril 2024      | ~4 meses  |
| 3.0.1  | Maio 2024       | ~1 mes    |

**Analise:**

- O projeto **consegue** entregar releases com certa regularidade
- Houve um gap significativo entre 3.0.1 (Maio 2024) e o ultimo commit (Novembro 2025)
- O projeto parece estar em modo de **manutencao reduzida**, com foco principal na plataforma hospedada da OpenAI

**Ultimo Commit Significativo:** 03/11/2025 - "Remove incontext_rl suite with defunct dependencies"

### 6.3 Barreira de Entrada para Novos Contribuidores

**Aspectos Positivos:**

1. Documentacao clara no README sobre como configurar o ambiente
2. Pre-commit hooks ajudam a manter padrao de codigo
3. Templates de PR detalhados (embora desatualizados)
4. Exemplos de evals disponiveis para referencia

**Aspectos Negativos:**

1. **PRs externos requerem aprovacao manual** para executar CI
2. Template de PR menciona "GPT-4 access" como incentivo (desatualizado)
3. Issue #1608 reporta que o template de PR esta obsoleto
4. Dependencia de `OPENAI_API_KEY` para executar testes completos
5. Testes unitarios falhando no main (Run #1808) pode confundir novatos

**Experiencia do Novo Contribuidor:**

```
1. Fork do repositorio              ✓ Facil
2. Clone e setup local              ✓ Documentado
3. Instalar pre-commit hooks        ✓ Instrucoes claras
4. Criar nova eval                  ~ Requer chave API
5. Abrir PR                         ✓ Template disponivel
6. Aguardar CI                      ✗ Requer aprovacao manual
7. Receber feedback                 ~ Pode demorar
8. Merge                            ~ Depende de revisores
```

---

## 7. Evidencias Coletadas

### 7.1 Issues Relevantes

| Issue | Titulo                                                   | Relevancia                         |
| ----- | -------------------------------------------------------- | ---------------------------------- |
| #1608 | Pull request template is obsolete                        | Template de PR desatualizado       |
| #1606 | Update python version in GitHub workflows to python 3.12 | CI usa Python 3.9 (desatualizado)  |
| #1605 | Remove incontext_rl suite with defunct dependencies      | Dependencias defeituosas removidas |

### 7.2 Pull Requests Relevantes

| PR    | Status                   | Observacao                               |
| ----- | ------------------------ | ---------------------------------------- |
| #1607 | Aberto (Action Required) | PR externo aguardando aprovacao          |
| #1605 | Merged                   | Mergeado apesar de falha posterior no CI |
| #1603 | Aberto                   | Eval submission aguardando revisao       |

### 7.3 Workflow Runs Recentes

| Run   | Workflow       | Status          | Duracao |
| ----- | -------------- | --------------- | ------- |
| #1811 | Run unit tests | Action Required | -       |
| #1808 | Run unit tests | **Failure**     | 12m 9s  |
| #2295 | Run new evals  | Success         | 10m 18s |
| #1807 | Run unit tests | **Failure**     | 12m 1s  |
| #1788 | Run unit tests | Success         | 3m 41s  |

---

## 8. Recomendacoes de Melhoria

### 8.1 Melhorias Prioritarias

1. **Adicionar Branch Protection Rules**
   - Exigir CI verde antes de permitir merge
   - Prevenir regressoes como observado no Run #1808

2. **Atualizar Versao do Python**
   - Migrar de Python 3.9 para 3.12
   - PR #1607 ja propoe essa mudanca

3. **Atualizar Template de PR**
   - Remover referencias obsoletas a "GPT-4 access"
   - Modernizar instrucoes de contribuicao

4. **Adicionar Metricas de Cobertura**
   - Integrar com codecov ou similar
   - Definir threshold minimo de cobertura

### 8.2 Melhorias Secundarias

5. **Adicionar Workflow de Linting**
   - Executar pre-commit hooks no CI (nao apenas localmente)
   - Garantir consistencia mesmo sem setup local

6. **Automatizar Release Notes**
   - Gerar changelog automaticamente
   - Facilitar rastreamento de mudancas

7. **Adicionar Testes de Integracao**
   - Testar fluxos completos de avaliacao
   - Aumentar confianca em refatoracoes

---

## 9. Conclusao

O projeto OpenAI Evals **implementa CI/CD de forma basica mas funcional**, utilizando GitHub Actions para testes automaticos e pre-commit hooks para qualidade de codigo. No entanto, existem lacunas significativas:

**Pontos Fortes:**

- Pipeline de CI configurado e executando
- Pre-commit hooks abrangentes
- Tempo de feedback razoavel (3-12 min)

**Pontos Fracos:**

- Ausencia de branch protection efetiva
- Testes falhando no main sem bloqueio
- Configuracoes desatualizadas (Python 3.9, templates)
- Barreira alta para contribuidores externos

**Impacto na Evolucao:**
A infraestrutura atual **facilita parcialmente** a evolucao segura do software, mas a falta de protecoes rigorosas permite que codigo potencialmente quebrado seja mergeado. Isto pode desincentivar grandes refatoracoes e reduzir a confianca dos desenvolvedores no pipeline.

---

## 10. Referencias

- Repositorio OpenAI Evals: https://github.com/openai/evals
- Workflows: https://github.com/openai/evals/actions
- Pre-commit Config: https://github.com/openai/evals/blob/main/.pre-commit-config.yaml
- Run Tests Workflow: https://github.com/openai/evals/blob/main/.github/workflows/run_tests.yaml
- Test Eval Workflow: https://github.com/openai/evals/blob/main/.github/workflows/test_eval.yaml

---

## Anexos

### A. Diagrama do Pipeline (Versao Simplificada)

```
Push/PR → Checkout → Setup Python → Install Deps → Run Tests → Pass/Fail
```

### B. Links para Evidencias

1. [Workflow Run #1808 (Falha no Main)](https://github.com/openai/evals/actions/runs/19050110253)
2. [PR #1607 (Action Required)](https://github.com/openai/evals/pull/1607)
3. [Issue #1608 (Template Obsoleto)](https://github.com/openai/evals/issues/1608)
4. [PR #1605 (Mergeado)](https://github.com/openai/evals/pull/1605)

---

_Documento gerado como parte da Atividade 3 da disciplina de Evolucao de Software 2025.2_
