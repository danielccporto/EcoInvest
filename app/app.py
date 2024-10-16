import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai')))

import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
from llm_tasks import sentiment_analysis, generate_summary, answer_question, generate_text


@st.cache_data
def load_financial_data(ticker):
    return yf.download(ticker, start="2023-01-01", end="2023-12-31")

@st.cache_data
def load_g1_news():
    try:
        return pd.read_csv("data/g1_economia_news.csv")
    except FileNotFoundError:
        st.error("Arquivo CSV de notícias não encontrado.")
        return pd.DataFrame()  # Retorna um DataFrame vazio caso não exista o arquivo CSV

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Funções para páginas
def financial_data_page():
    st.header("Amostra de Dados Financeiros")
    ticker = "AAPL"  # Especificar o ticker desejado
    data = load_financial_data(ticker)  # Carregar diretamente da API Yahoo Finance
    st.dataframe(data.tail())  # Exibir os dados mais recentes

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
    st.title("Ferramentas de Inteligência Artificial (LLMs)")

    # Análise de Sentimentos
    st.header("Análise de Sentimentos")
    text = st.text_area("Digite o texto para análise de sentimentos:")
    if st.button("Analisar Sentimento"):
        result = sentiment_analysis(text)
        st.write(result)

    # Geração de Resumos
    st.header("Geração de Resumos")
    summary_text = st.text_area("Digite o texto para gerar um resumo:")
    if st.button("Gerar Resumo"):
        summary = generate_summary(summary_text)
        st.write(summary)

    # Perguntas e Respostas
    st.header("Perguntas e Respostas (Q&A)")
    question = st.text_input("Digite a pergunta:")
    context = st.text_area("Digite o contexto da pergunta:")
    if st.button("Responder Pergunta"):
        answer = answer_question(question, context)
        st.write(answer)

    # Geração de Texto
    st.header("Geração de Texto com LLMs")
    prompt = st.text_area("Digite o prompt para gerar texto:")
    if st.button("Gerar Texto"):
        generated_text = generate_text(prompt)
        st.write(generated_text)

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
