# Avaliação do módulo de Operacionalização de Machine Learning - Projecto Individual

## Rumos Bank Going Live

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
│   └── prediction_service.py                    # Serviço de predição
├── tests/                  # Testes do projeto
└── .github/
    └── workflows/          # Workflows do GitHub Actions
        └── ci-cd.yml      # Pipeline de CI/CD
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

### Testes

Os testes são executados automaticamente em cada push e pull request. O ambiente de testes inclui:
- pytest com relatório de cobertura
- Cliente de testes FastAPI
- Testes de integração MLflow

Dependências necessárias para testes:
```bash
fastapi
uvicorn
httpx
mlflow
pytest
pytest-cov
```

### Implantação Docker

A aplicação está containerizada e é publicada automaticamente no GitHub Container Registry após builds bem-sucedidos.
Para baixar a imagem mais recente:

```bash
docker pull ghcr.io/<username>/prediction-service:latest
```

## Serviço de Predição

O serviço de predição está containerizado e disponível no GitHub Container Registry. Para utilizá-lo:

1. Pull da imagem mais recente:
   ```bash
   docker pull ghcr.io/paulofcamara/oml-trabalho/prediction-service:latest
   ```

2. Execute o serviço:
   ```bash
   docker-compose up -d
   ```

3. Verifique o status do serviço:
   ```bash
   curl http://localhost:8000/health
   ```

4. Envie requisições para o endpoint de predição:
   ```bash
   curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"features": {
       "LIMIT_BAL": 20000,
       "SEX": 2,
       "EDUCATION": 2,
       "MARRIAGE": 1,
       "AGE": 24,
       "PAY_0": 2,
       "PAY_2": 2,
       "PAY_3": -1,
       "PAY_4": -1,
       "PAY_5": -2,
       "PAY_6": -2,
       "BILL_AMT1": 3913,
       "BILL_AMT2": 3102,
       "BILL_AMT3": 689,
       "BILL_AMT4": 0,
       "BILL_AMT5": 0,
       "BILL_AMT6": 0,
       "PAY_AMT1": 0,
       "PAY_AMT2": 689,
       "PAY_AMT3": 0,
       "PAY_AMT4": 0,
       "PAY_AMT5": 0,
       "PAY_AMT6": 0
     }}'
   ```

5. O serviço retornará a predição em formato JSON:
   ```json
   {
     "prediction": 1,
     "probability": 0.75,
     "threshold": 0.5
   }
   ```

## Resultados do Modelo

O modelo final (Random Forest) alcançou:
- Redução de custos de €3.9M para €2.47M
- Features mais importantes: PAY_0 (status de pagamento atual) e AGE
- Threshold otimizado: 0.3 para melhor equilíbrio custo/benefício

## Pipeline de CI/CD

O projeto inclui um pipeline de CI/CD completo que:
- Executa testes automatizados com relatório de cobertura
- Constrói e publica o container Docker no GitHub Container Registry


### Informações do Autor

Este projeto foi desenvolvido por **Paulo Camara**.  
Email para contato: [paulo.f.camara@gmail.com](mailto:paulo.f.camara@gmail.com)

### Data limite de entrega

01/05/2025

Deve ser enviada, até à data limite de entrega, um link para o vosso github (tem de estar público). Podem enviar este link para o meu email `lopesg.miguel@gmail.com` ou slack.
