# MY APP FILE

import streamlit as st
import yfinance as yf
import pandas as pd

# Título do Projeto
st.title("EcoInvest: Plataforma de Investimentos Sustentáveis")

# Descrição do Problema
st.header("Descrição do Problema")
st.write("""
A EcoInvest tem como objetivo fornecer uma plataforma que ajude investidores a entender o impacto ESG
de suas decisões financeiras, promovendo práticas sustentáveis no mercado de capitais.
""")

# Links Úteis
st.header("Links Úteis")
st.markdown("[Relatório da ONU sobre Finanças Sustentáveis](https://www.un.org/sustainabledevelopment/)")

# Amostra de Dados Financeiros
st.header("Amostra de Dados Financeiros")
ticker = "AAPL"
data = yf.download(ticker, start="2023-01-01", end="2023-12-31")
st.dataframe(data.tail())

# Amostra de Dados ESG (Dados Fictícios)
st.header("Amostra de Dados ESG")
esg_data = {
    'Empresa': ['Apple', 'Microsoft', 'Tesla'],
    'Pontuação ESG': [75, 82, 68]
}
esg_df = pd.DataFrame(esg_data)
st.dataframe(esg_df)