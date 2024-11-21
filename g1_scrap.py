import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from ai.llm_tasks import sentiment_analysis, generate_summary



# Função para fazer o web scraping das notícias do G1 Economia
def scrape_g1_economia():
    url = "https://g1.globo.com/economia/"
    
    # Fazer a requisição HTTP para baixar o conteúdo da página
    response = requests.get(url)
    
    # Verificar o código de status da resposta
    if response.status_code != 200:
        print(f"Erro ao acessar a página. Status code: {response.status_code}")
        return None
    
    # Parsear o conteúdo da página com BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Lista para armazenar os dados dos artigos
    articles = []

    # Loop através de todos os artigos da página
    for item in soup.find_all("div", class_="feed-post-body"):
        title = item.find("a", class_="feed-post-link").text.strip()
        link = item.find("a", class_="feed-post-link")['href']
        summary = item.find("div", class_="feed-post-body-resumo").text.strip() if item.find("div", class_="feed-post-body-resumo") else "Sem resumo"
        
        # Adicionar o título, link e resumo à lista de artigos
        articles.append({
            "Title": title,
            "Summary": summary,
            "Link": link
        })

    # Verificar se encontramos artigos
    if len(articles) == 0:
        print("Nenhum artigo encontrado. Verifique os seletores CSS.")
        return None
    
    # Criar um DataFrame com os dados extraídos
    df = pd.DataFrame(articles)
    
    # Salvar o DataFrame em um arquivo CSV no diretório `data/`
    if not os.path.exists('data'):
        os.makedirs('data')  # Criar diretório data, se não existir
    
    df.to_csv("data/g1_economia_news.csv", index=False)
    print("Extração concluída e dados salvos em data/g1_economia_news.csv.")
    
    return df

# Testar o scraping
scrape_g1_economia()

# Exemplo: Processa uma notícia do G1
news_title = "Brasileiros gastaram neste ano cerca de R$ 20 bilhões por mês em apostas online, estima BC"
news_summary = generate_summary(news_title)
news_sentiment = sentiment_analysis(news_title)

print(f"Resumo: {news_summary}")
print(f"Sentimento: {news_sentiment}")