from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict
from transformers import pipeline
import pandas as pd
import yfinance as yf
import os
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.models import ProcessedTextResponse, ErrorResponse
import logging 


#config do logger 
logging.basicConfig(level=logging.DEBUG)


app = FastAPI()


# Inicializar modelos com tratamento de erros
try:
    sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

except Exception as e:
    logging.error(f"Erro ao carregar os modelos: {e}")
    sentiment_pipeline = None
    summarization_pipeline = None   



class TextInput(BaseModel):
    text: str

router = APIRouter()

# Tratamento de exceções globais
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Erro inesperado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Erro interno no servidor", "details": str(exc)},
    )


@router.post("/processar_texto", response_model=ProcessedTextResponse)
async def processar_texto(texto: str, tipo_analise: str):
    try:
        # Processamento do texto (simulado aqui)
        resultados = {"palavras": len(texto.split()), "caracteres": len(texto)}
        return ProcessedTextResponse(
            text=texto,
            analysis_type=tipo_analise,
            results=resultados,
            success=True,
            message = "Processamento de texto concluído com sucesso."
            )
    except Exception as e:
        logging.error(f"Erro ao processar texto: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar o texto: {str(e)}")

#Rota para análise de sentimentos
@app.post("/analyze_sentiment", response_model=ProcessedTextResponse)
def analyze_sentiment(data: TextInput):
    if not data.text or not data.text.strip():
        raise HTTPException(
            status_code=400,
            detail="O texto fornecido está vazio ou contém apenas espaços."
        )
    try:
        result = sentiment_pipeline(data.text)
        return {
            "text": data.text,
            "analysis_type": "sentiment_analysis",
            "results": {"label": result[0]["label"], "score": result[0]["score"]},
            "success": True,
            "message": "Análise de sentimento concluída com sucesso."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar a análise de sentimentos: {str(e)}")
    
# Rota para geração de resumos
@app.post("/generate_summary", response_model=ProcessedTextResponse)
def generate_summary(data: TextInput):
    if not data.text or not data.text.strip():
        raise HTTPException(
            status_code=400,
            detail="O texto fornecido está vazio ou contém apenas espaços."
        )
    try:
        result = summarization_pipeline(data.text, max_length=100, min_length=30, do_sample=False)
        return {
            "text": data.text,
            "analysis_type": "summarization",
            "results": {"summary": result[0]["summary_text"]},
            "success": True,
            "message": "Resumo gerado com sucesso."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar o resumo: {str(e)}")


# Função para carregar dados financeiros
def load_financial_data(ticker: str):
    try:
        # Tenta baixar os dados financeiros
        data = yf.download(ticker, start="2023-01-01", end="2023-12-31")
        if data.empty:
            raise ValueError(f"Ticker '{ticker}' não retornou dados financeiros.")
        return data
    except Exception as e:
        raise ValueError(f"Erro ao carregar dados financeiros para o ticker '{ticker}': {str(e)}")

# Rota para acessar dados financeiros
@app.get("/financial_data/{ticker}")
def get_financial_data(ticker: str):
    try:
        data = load_financial_data(ticker)
        return data.reset_index().to_dict(orient="records")
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar dados financeiros: {str(e)}")


# Rota para acessar dados do CSV de notícias do G1
@app.get("/news_data")
def get_news_data():
    try:
        # Verifica se o arquivo CSV existe no diretório
        if os.path.exists("data/g1_economia_news.csv"):
            data = pd.read_csv("data/g1_economia_news.csv")
            return data.to_dict(orient="records")
        else:
            raise HTTPException(status_code=404, detail="Arquivo CSV de notícias não encontrado.")
    except Exception as e:
        logging.error(f"Erro ao carregar dados do CSV de notícias: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados de notícias: {str(e)}")

# Rota para fazer upload de dados e salvar no servidor
@app.post("/upload_data")
def upload_data(data: list):
    # Verificar se os dados enviados são uma lista e não estão vazios
    if not isinstance(data, list) or len(data) == 0:
        raise HTTPException(
            status_code=400,
            detail="Os dados enviados devem ser uma lista não vazia."
        )
    try:
        # Tentar converter os dados para um DataFrame
        df = pd.DataFrame(data)
        if df.empty:
            raise ValueError("Os dados fornecidos resultaram em um DataFrame vazio.")
        # Salvar os dados em um arquivo CSV
        df.to_csv("data/uploaded_data.csv", index=False)
        return {"message": "Dados recebidos e salvos com sucesso."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar dados: {str(e)}")


@app.get("/uploaded_data")
def get_uploaded_data():
    try:
        if os.path.exists("data/uploaded_data.csv"):
            data = pd.read_csv("data/uploaded_data.csv")
            return data.to_dict(orient="records")
        else:
            raise HTTPException(status_code=404, detail="Arquivo de dados carregados não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar os dados carregados: {str(e)}")


