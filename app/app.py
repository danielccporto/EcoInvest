import streamlit as st
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Cachear a função que carrega os dados de finanças e ESG
@st.cache_data
def load_financial_data(ticker):
    return yf.download(ticker, start="2023-01-01", end="2023-12-31")

@st.cache_data
def load_g1_news():
    try:
        return pd.read_csv("data/g1_economia_news.csv")
    except FileNotFoundError:
        st.error("Arquivo CSV de notícias não encontrado. Execute o scraping para gerar o arquivo.")
        return pd.DataFrame()  # Retorna um DataFrame vazio caso não exista o arquivo CSV

# Função para converter DataFrame em CSV para download
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Iniciar a sessão
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False
    st.session_state['data_g1'] = pd.DataFrame()

# Título da aplicação
st.title("EcoInvest: Plataforma de Investimentos Sustentáveis")

# Links úteis
st.header("Links Úteis")
st.markdown("[Relatório da ONU sobre Finanças Sustentáveis](https://www.un.org/sustainabledevelopment/)")

# ------------------- Amostra de Dados Financeiros (com cache) ------------------
st.header("Amostra de Dados Financeiros")
ticker = "AAPL"
data = load_financial_data(ticker)
st.dataframe(data.tail())

# ----------------------- Amostra de Dados ESG -----------------------
st.header("Amostra de Dados ESG")
esg_data = {
    'Empresa': ['Apple', 'Microsoft', 'Tesla'],
    'Pontuação ESG': [75, 82, 68]
}
esg_df = pd.DataFrame(esg_data)
st.dataframe(esg_df)

# Seletor de tipo de investimento e slider para pontuação ESG
investment_type = st.selectbox("Escolha o tipo de investimento:", ["Ações", "Obrigações", "Fundos"])
esg_score = st.slider("Escolha a pontuação ESG desejada:", 0, 100, (20, 80))
st.write(f"Você selecionou {investment_type} com pontuação ESG entre {esg_score[0]} e {esg_score[1]}")

# --------------------- Carregar as notícias do G1 ---------------------
if not st.session_state['data_loaded']:
    st.session_state['data_g1'] = load_g1_news()
    st.session_state['data_loaded'] = True

data_g1 = st.session_state['data_g1']

# Exibir as notícias de economia e sustentabilidade do G1
st.title("Notícias de Economia e Sustentabilidade - G1")
st.write("Últimas notícias da economia, com foco em sustentabilidade:")
st.dataframe(data_g1)

for index, row in data_g1.iterrows():
    st.markdown(f"### {row['Title']}")
    st.write(row['Summary'])
    st.markdown(f"[Leia mais]({row['Link']})")

# ----------------------- Upload de arquivo CSV -----------------------
uploaded_file = st.file_uploader("Faça upload de um arquivo CSV", type=["csv"])
if uploaded_file:
    user_data = pd.read_csv(uploaded_file)
    st.write("Dados do arquivo carregado:")
    st.dataframe(user_data)

    # Combinar os dados do upload com os dados ESG já existentes
    combined_data = pd.concat([esg_df, user_data], ignore_index=True)
    
    st.write("Dados combinados:")
    st.dataframe(combined_data)

    # Permitir download dos dados combinados
    csv_combined = convert_df_to_csv(combined_data)
    st.download_button(
        label="Download dos Dados Combinados",
        data=csv_combined,
        file_name='dados_combinados.csv',
        mime='text/csv',
    )

# ---------------------- Download de dados em CSV ----------------------
if not data_g1.empty:
    csv = convert_df_to_csv(data_g1)
    st.download_button(
        label="Download dos Dados em CSV",
        data=csv,
        file_name='g1_economia_news.csv',
        mime='text/csv',
    )
