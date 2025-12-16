# Regras do Dataset – Finanças Pessoais

## Formato geral
- Arquivo: CSV
- Codificação: UTF-8
- Separador: vírgula
- Datas no formato: YYYY-MM-DD

## Colunas

### data
- Tipo: data
- Obrigatória
- Representa a data da transação

### descricao
- Tipo: texto
- Obrigatória
- Exemplo: Uber, Mercado, Spotify

### categoria
- Tipo: texto
- Obrigatória
- Exemplos: alimentação, transporte, assinaturas

### conta
- Tipo: texto
- Obrigatória
- Exemplo: inter, nubank, dinheiro

### tipo
- Tipo: texto
- Valores permitidos: despesa | receita

### valor
- Tipo: numérico (float)
- Sempre positivo
- O sinal é definido pela coluna `tipo`

### forma_pagamento
- Tipo: texto
- Exemplos: pix, crédito, débito, dinheiro

### parcelas_total
- Tipo: inteiro
- Padrão: 1

### parcela_atual
- Tipo: inteiro
- Padrão: 1

### tags
- Tipo: texto
- Exemplos: fixo, lazer, necessário
``
