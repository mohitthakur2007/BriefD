from flask import Flask, render_template, request, jsonify
import requests
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load API keys from environment
api_key = os.getenv('MEDIASTACK_API_KEY', '29bfd055173557c9ca946a8cb98343a7')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Function to fetch news from Mediastack API
def get_news(api_key, query='business', count=10):
    url = 'https://api.mediastack.com/v1/news'
    params = {
        'access_key': api_key,
        'categories': query,
        'limit': count
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        news_data = response.json()
        articles = news_data.get('data', [])
        
        return articles if articles else []
    except requests.exceptions.Timeout:
        print("API request timed out")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

# Function to summarize and translate using Gemini
def summarize_with_gemini(text, language='English'):
    if not GEMINI_API_KEY:
        return "Gemini API key not configured"
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""Please summarize this news article in 2-3 short sentences and translate to {language}.
    
Article:
{text}

Provide only the summary in {language}, no additional text."""
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        summary = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Summary unavailable')
        return summary
    except Exception as e:
        print(f"Gemini API error: {e}")
        return f"Error generating summary: {str(e)}"

# Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    query = 'business'
    page_size = 10
    
    if request.method == 'POST':
        query = request.form.get('category', 'business')
    
    try:
        # Get news articles
        news = get_news(api_key, query, page_size)
        trending_news = get_news(api_key, 'general', 8)  # Different category for trending
        
        if news:
            random.shuffle(news)
            selected_news = [{
                'title': article.get('title', 'No title'),
                'description': article.get('description', 'No description available'),
                'url': article.get('url', '#'),
                'image_url': article.get('image', ''),
                'source': article.get('source', 'Unknown'),
                'published_at': article.get('published_at', '')
            } for article in news[:10]]
        else:
            selected_news = []
        
        if trending_news:
            trending_news = [{
                'title': article.get('title', 'No title'),
                'description': article.get('description', ''),
                'url': article.get('url', '#'),
                'source': article.get('source', 'Unknown')
            } for article in trending_news[:8]]
        else:
            trending_news = []
        
        return render_template('index.html', news=selected_news, trending_news=trending_news, categories=categories, query=query)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('index.html', error=f'Error fetching news: {str(e)}', categories=categories, news=[], trending_news=[])

# API endpoint for AI summarization
@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    data = request.json
    text = data.get('text', '')
    language = data.get('language', 'English')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    summary = summarize_with_gemini(text, language)
    return jsonify({'summary': summary})

if __name__ == "__main__":
    app.run(debug=True)
