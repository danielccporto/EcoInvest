# EcoInvest  
A Sustainable Solution for Informed Investors  

EcoInvest integrates data science and artificial intelligence to promote sustainable investments aligned with ESG practices. Through an interactive dashboard, it provides relevant insights that transform complex data into actionable information.  

## Key Features  

### Sentiment Analysis  
Evaluates the emotional impact of economic news.  

### Summary Generation  
Simplifies information from lengthy news articles.  

### Intelligent Recommendations  
Suggests actions based on ESG and financial data.  

### Interactive Dashboard  
Combines charts and tables to explore data and insights effectively.  

## Technologies Used  

- **Streamlit**: Interactive dashboard.  
- **FastAPI**: Robust RESTful API.  
- **Beautiful Soup**: Web scraping.  
- **Hugging Face Transformers**: Natural language modeling.  
- **Pandas and Matplotlib**: Data analysis and visualization.  

## Steps to Run the App  

### 1. Clone the Repository  
```bash
git clone https://github.com/your-username/EcoInvest.git

#### 2. Create and Activate a Virtual Environment
- python -m venv venv

##### Activate the virtual environment:
- Windows: venv\Scripts\activate
- Mac/Linux: source venv/bin/activate

#### 3. Install Dependencies
- pip install -r requirements.txt

#### 4. Run the Backend (FastAPI)
- uvicorn app.services.api:app --reload
The backend will be available at: http://127.0.0.1:8000

#### 5. Run the Frontend (Streamlit)
- streamlit run app/app.py
The frontend will be available at: http://localhost:8501

##### Notes
Ensure the backend is running before accessing the dashboard in your browser.
Data files such as g1_economia_news.csv, esg_data.csv, and finance_data.csv should be present in the data/ folder.






