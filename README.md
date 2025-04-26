# Avaliação do módulo de Operacionalização de Machine Learning - Projecto Individual

## Rumos Bank going live

O Rumos Bank é um banco que tem perdido bastante dinheiro devido à quantidade de créditos que fornece e que não são pagos dentro do prazo devido. 

Depois do banco te contratar, como data scientist de topo, para ajudares a prever os clientes que não irão cumprir os prazos, os resultados exploratórios iniciais são bastante promissores!

Mas o banco está algo receoso, já que teve uma má experiência anterior com uma equipa de data scientists, em que a transição dos resultados iniciais exploratórios até de facto conseguirem ter algo em produção durou cerca de 6 meses, bem acima da estimativa inicial.

Por causa desta prévia má experiência, o banco desta vez quer ter garantias que a passagem dos resultados iniciais para produção é feita de forma mais eficiente. O objetivo é que a equipa de engenharia consiga colocar o vosso modelo em produção em dias em vez de meses!

## Avaliação

Os componentes que vão ser avaliados neste projecto são:

* Todas as alterações que fazem são trackeadas num repositório do github
* `README.md` atualizado
* Ambiente do projecto (conda.yaml) definido de forma adequada
* Runs feitas no notebook `rumos_bank_leading_prediction.ipynb` estão documentadas, reproduzíveis, guardadas e facilmente comparáveis
* Os modelos utilizados estão registados e versionados num Model Registry
* O melhor modelo está a ser servido num serviço - não precisa de UI
* O serviço tem testes
* O serviço está containerizado
* O container do serviço é built, testado e enviado para um container registry num pipeline de CICD

Garantam que tanto o repositório do github como o package no github estão ambos públicos!

## Estrutura do Projeto

```
.
├── conda.yaml              # Definição do ambiente Conda
├── requirements.txt        # Dependências Python
├── data/                   # Dados do projeto
│   └── lending_data.csv    # Dataset do banco
├── mlruns/                 # Diretório central do MLflow para tracking
├── notebooks/             
│   ├── rumos_bank_lending_prediction.ipynb      # Notebook principal
│   ├── loan_default_pipeline_mlflow.ipynb       # Pipeline com MLflow
│   └── serve/                                   # Notebooks para teste do serviço
├── src/
│   ├── mlflow_initializer.py                    # Configuração centralizada do MLflow
│   └── prediction_service.py                   # Serviço de predição
└── tests/                  # Testes do projeto
```

## Configuração do MLflow

O projeto utiliza MLflow para tracking de experimentos, com as seguintes configurações:

- Tracking URI: `http://localhost:5000` (servidor remoto containerizado)
- Experiment Name: "bank_lending_prediction"
- Model Registry gerido remotamente no servidor MLflow

Para inicializar o MLflow em notebooks:

```python
import mlflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("bank_lending_prediction")
```

## Serviço de Predição

O serviço de predição está containerizado e pode ser acessado via API. Para utilizá-lo:

1. Certifique-se de que o serviço está em execução:
   ```bash
   docker-compose up -d
   ```

2. Envie requisições para o endpoint de predição:
   ```bash
   curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"data": [[30, 2, 1, 20000, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]}'
   ```

3. O serviço retornará a predição do modelo em formato JSON.

## Quick-Start

### Criar e ativar o ambiente Conda

```bash
conda env create -f conda.yaml
conda activate oml-trabalho
```

### Instalar dependências com pip (opcional)

Para utilizadores sem Conda:

```bash
pip install -r requirements.txt
```

### Informações do Autor

Este projeto foi desenvolvido por **Paulo Camara**.  
Email para contato: [paulo.f.camara@gmail.com](mailto:paulo.f.camara@gmail.com)

### Data limite de entrega

01/05/2025

Deve ser enviada, até à data limite de entrega, um link para o vosso github (tem de estar público). Podem enviar este link para o meu email `lopesg.miguel@gmail.com` ou slack.
