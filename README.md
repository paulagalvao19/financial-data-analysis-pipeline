Projeto Data Analyzer – Controle Financeiro Pessoal

Este projeto implementa um pipeline completo de análise de dados financeiros pessoais utilizando Python.
O sistema realiza leitura, validação, limpeza, transformação e análise dos dados, além da geração automática
de visualizações gráficas para apoio ao controle financeiro.

====================================================================

OBJETIVO

O objetivo do projeto é transformar registros financeiros brutos (CSV) em informações estruturadas,
permitindo a análise de gastos, receitas e saldo mensal, bem como a visualização dos principais padrões
financeiros ao longo do tempo.

====================================================================

ESTRUTURA DO PROJETO

projeto_data_analyzer/
├── dashboard/
│   ├── top_categorias.png
│   └── saldo_mensal.png
├── data/
│   ├── raw/
│   │   └── gastos.csv
│   └── processed/
│       └── gastos_limpos.csv
├── docs/
│   └── regras_dados.md
├── src/
│   └── main.py
└── README.md

====================================================================

ESTRUTURA DO CSV

O arquivo de entrada deve conter as seguintes colunas:

- data: data da transação
- descricao: descrição do gasto ou receita
- categoria: categoria financeira
- conta: conta utilizada
- tipo: receita ou despesa
- valor: valor monetário no formato brasileiro (ex: 1234,56)
- forma_pagamento: crédito, débito, transferência, etc.
- parcelas_total: número total de parcelas
- parcela_atual: parcela correspondente à linha
- tags: palavras-chave para classificação

O pipeline assume que os dados seguem este esquema para correta execução.

====================================================================

PIPELINE DE PROCESSAMENTO

O pipeline executa as seguintes etapas:

1. Leitura do arquivo CSV e verificação de existência
2. Padronização dos nomes das colunas
3. Validação das colunas obrigatórias
4. Conversão e tratamento de datas e valores
5. Criação de colunas auxiliares (ano, mês, dia)
6. Geração de valor assinado (despesas negativas, receitas positivas)
7. Cálculo de métricas financeiras
8. Geração de dashboards
9. Salvamento dos dados tratados

====================================================================

ANÁLISES REALIZADAS

- Resumo financeiro geral (receitas, despesas e saldo final)
- Top gastos por categoria
- Resumo mensal de receitas, despesas e saldo

====================================================================

DASHBOARDS GERADOS

O projeto gera automaticamente os seguintes gráficos:

1. Top gastos por categoria
   - Gráfico de barras horizontais
   - Destaque visual para maior, médio e menor impacto financeiro

2. Evolução do saldo mensal
   - Gráfico de linha temporal
   - Destaque para o melhor e pior mês
   - Linha de referência no saldo zero

Os gráficos são salvos na pasta "dashboard".

====================================================================

COMO EXECUTAR O PROJETO

1. Instalar as dependências necessárias:

pip install pandas matplotlib

2. Executar o pipeline:

python src/main.py

Após a execução:
- Os dados tratados estarão disponíveis em data/processed
- Os gráficos estarão disponíveis em dashboard

====================================================================

TECNOLOGIAS UTILIZADAS

- Python
- Pandas
- Matplotlib
- Manipulação de arquivos com os

====================================================================

POSSÍVEIS EVOLUÇÕES

- Dashboard interativo com Streamlit
- Exportação de relatórios em PDF ou HTML
- Análises por forma de pagamento
- Análises de compras parceladas
- Automatização de atualização mensal dos dados

====================================================================

AUTORIA

Projeto desenvolvido para fins de aprendizado e construção de portfólio em análise de dados com Python.
