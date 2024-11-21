import sys
import os
import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
from pydantic import BaseModel

# Caminho para funções externas 

from app.models.models import ProcessedTextResponse, ErrorResponse


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai')))
from ai.llm_tasks import sentiment_analysis, generate_summary

@st.cache_data
def load_financial_data(ticker):
    return yf.download(ticker, start="2023-01-01", end="2023-12-31")

@st.cache_data
def load_g1_news():
    try:
        return pd.read_csv("data/g1_economia_news.csv")
    except FileNotFoundError:
        st.error("Arquivo CSV de notícias não encontrado.")
        return pd.DataFrame()  
    
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Funções para páginas
def financial_data_page():
    st.header("Amostra de Dados Financeiros")
    ticker = "AAPL"  
    data = load_financial_data(ticker)  
    st.dataframe(data.tail())  

def esg_data_page():
    st.header("Amostra de Dados ESG")
    esg_data = {'Empresa': ['Apple', 'Microsoft', 'Tesla'], 'Pontuação ESG': [75, 82, 68]}
    esg_df = pd.DataFrame(esg_data)
    st.dataframe(esg_df)
    investment_type = st.selectbox("Escolha o tipo de investimento:", ["Ações", "Obrigações", "Fundos"])
    esg_score = st.slider("Escolha a pontuação ESG desejada:", 0, 100, (20, 80))
    st.write(f"Você selecionou {investment_type} com pontuação ESG entre {esg_score[0]} e {esg_score[1]}")

def news_page():
    st.title("Notícias de Economia e Sustentabilidade - G1")
    data_g1 = st.session_state['data_g1']
    st.write("Últimas notícias:")
    page_size = 10
    for start in range(0, len(data_g1), page_size):
        sub_data = data_g1[start:start + page_size]
        st.dataframe(sub_data)
        if st.button("Carregar mais", key=f"page_{start}"):
            break

def upload_page():
    uploaded_file = st.file_uploader("Faça upload de um arquivo CSV", type=["csv"])
    if uploaded_file:
        user_data = pd.read_csv(uploaded_file)
        st.write("Dados carregados:")
        st.dataframe(user_data)
        esg_data = {'Empresa': ['Apple', 'Microsoft', 'Tesla'], 'Pontuação ESG': [75, 82, 68]}
        esg_df = pd.DataFrame(esg_data)
        combined_data = pd.concat([esg_df, user_data], ignore_index=True)
        st.dataframe(combined_data)
        csv_combined = convert_df_to_csv(combined_data)
        st.download_button("Download dos Dados Combinados", data=csv_combined, file_name='dados_combinados.csv', mime='text/csv')

def download_data_page():
    st.title("Download de Dados")
    if not st.session_state['data_g1'].empty:
        csv = convert_df_to_csv(st.session_state['data_g1'])
        st.download_button("Download em CSV", data=csv, file_name='g1_economia_news.csv', mime='text/csv')

# Nova página de Ferramentas de IA com LLMs
def ai_tools_page():
    st.title("Ferramentas de Inteligência Artificial (LLMs) via API")

    # Análise de Sentimentos
    st.header("Análise de Sentimentos")
    text = st.text_area("Digite o texto para análise de sentimentos:")
    if st.button("Analisar Sentimento"):
        response = requests.post("http://127.0.0.1:8000/analyze_sentiment", json={"text": text})
        if response.status_code == 200:
            try:
                data = ProcessedTextResponse(**response.json())
                st.write("Resultado:", data.results)
            except Exception as e:
                st.error(f"Erro no formato da resposta: {e}")
        else:
            st.error("Erro na análise de sentimentos.")

    # Geração de Resumos
    st.header("Geração de Resumos")
    summary_text = st.text_area("Digite o texto para gerar um resumo:")
    if st.button("Gerar Resumo"):
        response = requests.post("http://127.0.0.1:8000/generate_summary", json={"text": summary_text})
        if response.status_code == 200:
            try:
                data = ProcessedTextResponse(**response.json())
                st.write("Resumo:", data.results.get("summary"))
            except Exception as e:
                st.error(f"Erro no formato da resposta: {e}")
        else:
            st.error("Erro na geração de resumo.")

# Inicializar sessão e cache
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False
    st.session_state['data_g1'] = pd.DataFrame()

if not st.session_state['data_loaded']:
    st.session_state['data_g1'] = load_g1_news()
    st.session_state['data_loaded'] = True

# Menu de navegação
st.sidebar.title("Navegação")
page = st.sidebar.selectbox(
    "Selecione a página",
    ["Home", "Visualização de Dados Financeiros", "Pontuação ESG", "Notícias", "Upload de Arquivos", "Download de Dados", "Ferramentas de IA"]
)

def home_page():
    st.title("Bem-vindo ao EcoInvest")
    st.write("Escolha uma página no menu à esquerda para explorar os dados.")

# Definir as páginas
if page == "Home":
    home_page()
elif page == "Visualização de Dados Financeiros":
    financial_data_page()
elif page == "Pontuação ESG":
    esg_data_page()
elif page == "Notícias":
    news_page()
elif page == "Upload de Arquivos":
    upload_page()
elif page == "Download de Dados":
    download_data_page()
elif page == "Ferramentas de IA":
    ai_tools_page()
