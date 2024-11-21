from transformers import pipeline

# Inicializa pipelines globais
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

# Função de análise de sentimentos
def sentiment_analysis(text):
    return sentiment_pipeline(text)

# Função de geração de resumo
def generate_summary(text):
    return summarization_pipeline(text, max_length=100, min_length=30, do_sample=False)
