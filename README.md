# Case Técnico Data Science — iFood

Solução para o desafio de **distribuição inteligente de cupons e ofertas**: dado o histórico de
um teste de 30 dias (76 mil ofertas enviadas a 17 mil clientes), decidir **qual oferta enviar
para cada cliente** e estimar o impacto dessa política no negócio.

## Resumo da solução

1. **Processamento (PySpark)** — reconstrução da jornada de cada oferta enviada
   (recebida → visualizada → convertida), com dois cuidados centrais:
   - **atribuição**: oferta concluída sem ter sido visualizada não conta como conversão
     (o desconto foi pago sem influência do envio — ~30% dos descontos do teste);
   - **anti-vazamento**: as features de comportamento de cada envio usam apenas eventos
     estritamente anteriores àquele envio.
2. **Modelagem (scikit-learn)** — um **modelo único de propensão** `P(conversão | cliente, oferta)`
   (Gradient Boosting), validado com split agrupado por cliente. Com ele, pontuamos as 10 ofertas
   do portfólio para cada cliente e recomendamos a de maior propensão.
3. **Impacto** — como o envio do teste foi aleatório, os envios que coincidiram com a recomendação
   do modelo formam um quase-experimento natural.

| Métrica | Valor |
|---|---|
| ROC-AUC (teste, clientes nunca vistos) | **0,80** |
| Conversão da política atual (aleatória) | 38,6% |
| Conversão nos envios iguais à recomendação | **66,0%** (IC95% 63,6–68,3%) |
| Benchmark "melhor oferta única para todos" | 62,8% |
| Uplift estimado | **+27 p.p. (+71%)** vs atual |

## Entregáveis do case

| Pedido no case | Onde está |
|---|---|
| 1. Notebook de processamento de dados (PySpark) | [notebooks/1_data_processing.ipynb](notebooks/1_data_processing.ipynb) |
| 2. Notebook/script de modelagem (treino e avaliação) | [notebooks/2_modeling.ipynb](notebooks/2_modeling.ipynb) |
| 3. Apresentação (máx. 5 slides, para lideranças) | [presentation/apresentacao.html](presentation/apresentacao.html) |

Os notebooks estão versionados **já executados** (com outputs e gráficos), então os resultados
podem ser avaliados sem rodar nada.

## Estrutura do repositório

```
ifood-case/
├── data/
│   ├── raw/                     # dados originais (ver download abaixo; fora do git)
│   └── processed/               # saídas dos notebooks (fora do git):
│                                #   NB1: unified_dataset/offers/profile/transactions (parquet)
│                                #   NB2: propensity_model.joblib, model_results.json
├── notebooks/
│   ├── 1_data_processing.ipynb  # limpeza, jornada da oferta, dataset unificado (PySpark)
│   └── 2_modeling.ipynb         # EDA do target, modelo, política e impacto (scikit-learn)
├── presentation/
│   └── apresentacao.html        # 5 slides para lideranças de negócio
├── src/
│   ├── spark_utils.py           # sessão Spark local + utilitários
│   └── viz.py                   # estilo padrão dos gráficos
├── README.md
└── requirements.txt
```

## Como executar

Pré-requisitos: **Python 3.12**, **Java 17** (JDK) e, no Windows, o
[winutils](https://github.com/cdarlint/winutils) (`HADOOP_HOME` apontando para a pasta com
`bin/winutils.exe` e `bin/hadoop.dll`). Ajuste os caminhos padrão de `JAVA_HOME`/`HADOOP_HOME`
em [src/spark_utils.py](src/spark_utils.py) ou defina as variáveis de ambiente. Em Linux/macOS
basta o Java.

```bash
# 1. ambiente (uv — ou use python -m venv + pip)
uv venv
uv pip install -r requirements.txt
# ative: .venv\Scripts\activate (Windows) | source .venv/bin/activate (Linux/macOS)

# 2. dados: baixe o tar.gz e copie APENAS os 3 JSONs para data/raw/
#    (offers.json, profile.json, transactions.json — ignore os arquivos "._*" do macOS)
#    https://data-architect-test-source.s3.sa-east-1.amazonaws.com/ds-technical-evaluation-data.tar.gz

# 3. notebooks (nesta ordem — o notebook 2 consome as saídas do 1)
jupyter nbconvert --to notebook --execute --inplace notebooks/1_data_processing.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/2_modeling.ipynb
# (ou abra no Jupyter e rode célula a célula)
```

Ambiente testado: Python 3.12, PySpark 4.1.2 (Java 17), pandas 3.0, scikit-learn 1.9 — versões
pinadas em [requirements.txt](requirements.txt). O pipeline é determinístico (seeds fixas):
re-executar reproduz os mesmos números. Qualidade de código: notebooks e `src/` passam por
`ruff check` e `ruff format`.

A apresentação ([presentation/apresentacao.html](presentation/apresentacao.html)) abre direto no
navegador. O case recomenda Databricks Community Edition; a solução roda localmente com PySpark
puro e é portável para Databricks sem mudanças de lógica (a criação da sessão em
`src/spark_utils.py` torna-se desnecessária lá).

## Premissas principais

- `time_since_test_start` e `duration` estão em dias; a janela de validade de uma oferta recebida
  em `t` é `[t, t + duration]`.
- `age = 118` co-ocorre com `gender` e `credit_card_limit` nulos → cadastro sem demografia
  (mantido com flag `missing_profile`, não descartado).
- Conversão **exige visualização**; para ofertas `informational` (sem evento de conclusão),
  conversão = transação após a visualização, dentro da validade.
- Recebimentos repetidos da mesma oferta: cada visualização/conclusão é atribuída ao recebimento
  ativo mais recente.
- Como não há data de calendário nos eventos, o tempo de casa (`membership_days`) usa a maior
  data de cadastro da base como referência.

As justificativas de cada decisão, as limitações (propensão ≠ incrementalidade, recomendação de
teste A/B) e os próximos passos estão detalhados nos notebooks.
