from transformers import pipeline
import openai
import os 

# Função de análise de sentimentos
def sentiment_analysis(text):
    classifier = pipeline('sentiment-analysis')
    return classifier(text)

# Função de geração de resumo
def generate_summary(text):
    summarizer = pipeline('summarization')
    return summarizer(text, max_length=130, min_length=30, do_sample=False)

# Função de perguntas e respostas
def answer_question(question, context):
    qa_model = pipeline('question-answering')
    return qa_model({'question': question, 'context': context})

# Função para geração de texto com OpenAI GPT-3
def generate_text(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()