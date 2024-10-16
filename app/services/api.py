from fastapi import FastAPI
import pandas as pd
import yfinance as yf
import os

app = FastAPI()

# Função para carregar dados financeiros da API do Yahoo Finance
def load_financial_data(ticker):
    return yf.download(ticker, start="2023-01-01", end="2023-12-31")

# Exemplo de rota para acessar dados financeiros diretamente da API Yahoo Finance
@app.get("/financial_data/{ticker}")
def get_financial_data(ticker: str):
    try:
        data = load_financial_data(ticker)
        # Retorna os dados financeiros como um dicionário
        return data.to_dict(orient="records")
    except Exception as e:
        return {"error": f"Erro ao carregar dados financeiros: {str(e)}"}

# Rota para acessar dados do CSV de notícias do G1
@app.get("/news_data")
def get_news_data():
    try:
        # Verifica se o arquivo CSV existe no diretório
        if os.path.exists("data/g1_economia_news.csv"):
            data = pd.read_csv("data/g1_economia_news.csv")
            return data.to_dict(orient="records")
        else:
            return {"error": "Arquivo CSV de notícias não encontrado"}
    except Exception as e:
        return {"error": f"Erro ao carregar dados de notícias: {str(e)}"}

# Rota para fazer upload de dados e salvar no servidor
@app.post("/upload_data")
def upload_data(data: list):
    try:
        # Converte os dados recebidos para um DataFrame e salva em CSV
        df = pd.DataFrame(data)
        df.to_csv("data/uploaded_data.csv", index=False)
        return {"message": "Dados recebidos e salvos com sucesso"}
    except Exception as e:
        return {"error": f"Erro ao salvar dados: {str(e)}"}

# Exemplo de rota GET para retornar os dados carregados via POST (upload)
@app.get("/uploaded_data")
def get_uploaded_data():
    try:
        if os.path.exists("data/uploaded_data.csv"):
            data = pd.read_csv("data/uploaded_data.csv")
            return data.to_dict(orient="records")
        else:
            return {"error": "Arquivo de dados carregados não encontrado"}
    except Exception as e:
        return {"error": f"Erro ao carregar os dados carregados: {str(e)}"}
