# EcoInvest
## Uma Solução Sustentável para Investidores Informados
O EcoInvest integra ciência de dados e inteligência artificial para promover investimentos sustentáveis, alinhados às práticas de ESG. Por meio de um dashboard interativo, oferece insights relevantes que transformam dados complexos em informações acionáveis.

### Funcionalidades Principais
#### Análise de Sentimentos:
Avalia o impacto emocional de notícias econômicas.

#### Geração de Resumos:
Simplifica informações de notícias longas.

#### Recomendações Inteligentes:
Sugere ações baseadas em dados ESG e financeiros.

#### Dashboard Interativo:
Combina gráficos e tabelas para explorar os dados e insights.

#### Tecnologias Utilizadas
Streamlit: Dashboard interativo.
FastAPI: API RESTful robusta.
Beautiful Soup: Web scraping.
Hugging Face Transformers: Modelagem de linguagem natural.
Pandas e Matplotlib: Análise e visualização de dados.

### Passo a Passo para Rodar o App
#### 1. Clonar o Repositório
- git clone https://github.com/seu-usuario/EcoInvest.git

#### 2. Criar e Ativar um Ambiente Virtual
- python -m venv venv

##### Ative ambiente virtual:
- Windows: venv\Scripts\activate
- Mac/Linux: source venv/bin/activate

#### 3. Instalar as Dependências
- pip install -r requirements.txt

#### 4. Rodar o Backend (FastAPI)
- uvicorn app.services.api:app --reload
O backend estará disponível em: http://127.0.0.1:8000

#### 5. Rodar o Frontend (Streamlit)
- streamlit run app/app.py
O frontend estará disponível em: http://localhost:8501

##### Notas
Certifique-se de que o backend está rodando antes de acessar o dashboard no navegador.
Arquivos de dados, como g1_economia_news.csv, esg_data.csv e finance_data.csv, devem estar presentes na pasta data/.

