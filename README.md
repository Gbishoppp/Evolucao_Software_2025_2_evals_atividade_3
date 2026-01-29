# Evolucao_Software_2025-2_evals_atividade3

## 📘 Apresentação

Este repositório contém os materiais desenvolvidos pela equipe para a realização da atividade
**Evolucao_Software_2025_2_evals_atividade3**, da disciplina de Evolução de Software.

O objetivo é documentar e permitir a replicação da análise da infraestrutura de Integração Contínua (CI/CD)
do projeto openai/evals.

---

## 📌 Projeto Analisado

- Nome: OpenAI Evals
- Repositório Oficial: https://github.com/openai/evals
- Plataforma de CI/CD: GitHub Actions

---

## 👥 Integrantes da Equipe

| Nome                         | Matrícula      |
|------------------------------|---------------|
| Gabriel Bispo Santana        | 202000012702   |
| Pedro Savio Souza da Silva   | 202100114142   |
| Thiago Freire de Carvalho    | 202000013147   |

---

## 📄 Tutorial em PDF

O tutorial completo da atividade encontra-se disponível no arquivo:
Gabriel_Bispo_Santana_Pedro_Savio_Souza_da_Silva_Thiago_Freire_de_Carvalho_Atividade_3


O documento contém a análise detalhada, fluxograma do pipeline, avaliação de eficiência e contribuições
dos integrantes, conforme solicitado pela disciplina.

---

## 📂 Conteúdo do Repositório

Este repositório contém:

```
📁 Evolucao_Software_2025-2_evals_atividade3
 ├── 📄 main.py
 └── 📄 README.md
```



Onde:

- `main.py` → Script para análise automatizada dos workflows
- `README.md` → Documentação da atividade

---

## ⚙️ Metodologia

A equipe realizou as seguintes etapas:

1. Análise manual dos workflows do GitHub Actions.
2. Investigação da aba Actions e Pull Requests.
3. Desenvolvimento de script para apoio à análise.
4. Elaboração do tutorial em PDF.
5. Produção do vídeo explicativo.

---

## 🔁 Pipeline Analisado (Resumo)

O pipeline do projeto é acionado automaticamente quando ocorre um push ou a abertura de um Pull Request.

Etapas principais:

1. Checkout do código
2. Instalação de dependências
3. Execução de testes automáticos
4. Registro dos resultados
5. Retorno do status ao GitHub

Não há, publicamente, etapas automatizadas de lint, build Docker ou deploy.

---

## ▶️ Execução do Script

### Requisitos

- Python 3.8 ou superior
- Biblioteca requests

Instalação:

```
pip install requests
```
Execução:
```
python main.py
```
O script irá identificar os workflows do repositório e analisar suas principais etapas.

### Funcionalidades

O script realiza:

- Identificação de workflows  
- Leitura de arquivos YAML  
- Detecção de etapas de teste, build, lint, Docker e deploy  
- Geração de relatório no terminal

## Impacto na Evolução do Software

### Refatoração e Dívida Técnica

A presença de CI/CD automatizado aumenta a confiança dos desenvolvedores para realizar refatorações,
pois falhas são identificadas rapidamente.

### Frequência de Releases

O projeto apresenta histórico regular de atualizações, permitindo entrega contínua de valor aos usuários.

### Barreira de Entrada

O pipeline automatizado facilita a participação de novos contribuidores, validando automaticamente
suas contribuições.

---

## Contribuições dos Integrantes

| Integrante | Atividades Desenvolvidas |
|------------|--------------------------|
| Gabriel    | Análise geral, desenvolvimento do script, redação do relatório |
| Pedro      | Pesquisa técnica e apoio na análise |
| Thiago     | Revisão do material e apoio na produção do vídeo |

---

## Replicação da Atividade

Para reproduzir esta atividade:

1. Clone este repositório.
2. Instale as dependências.
3. Execute o script de análise.
4. Consulte o tutorial em PDF.
5. Compare os resultados obtidos.

---

## Vídeo da Atividade

O vídeo explicativo apresenta:

- Demonstração da análise no ambiente de desenvolvimento  
- Navegação pelo GitHub Actions  
- Apresentação do relatório  
- Explicação da metodologia  

O arquivo segue o padrão exigido pela disciplina.

---

## Data de Entrega

29/01/2026

---

## Observações Finais

Este repositório foi desenvolvido exclusivamente para fins acadêmicos, conforme orientações da atividade.
Não consiste em um clone do projeto analisado, mas sim em um conjunto de artefatos produzidos para fins
de documentação e replicação.

