from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Your Mediastack API key
api_key = '29bfd055173557c9ca946a8cb98343a7'

# Function to fetch news from Mediastack API
def get_news(api_key, query='business', count=10):
    url = 'http://api.mediastack.com/v1/news'
    params = {
        'access_key': api_key,
        'categories': query,
        'limit': count
    }
    
    try:
        # Sending the GET request to the API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
        
        # Parse the response JSON and extract articles
        news_data = response.json()
        articles = news_data.get('data', [])
        
        if not articles:
            print("No articles found for this query.")
        
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None

# Function to truncate text for better presentation
def truncate_text(text, word_limit=30):
    if not text:
        return ''  # Return empty string if the text is None
    words = text.split()
    if len(words) > word_limit:
        return ' '.join(words[:word_limit]) + '...'
    return text

# Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    query = 'business'  # Default search query (category)
    page_size = 10  # Limit number of articles displayed
    
    if request.method == 'POST':
        query = request.form.get('category', 'business')  # Get the selected category
    else:
        query = 'business'  # Default category on GET request
    
    try:
        # Get selected news based on query
        news = get_news(api_key, query, page_size)
        
        # Get trending news (same query as selected)
        trending_news = get_news(api_key, query, page_size)
        
        if news is not None:
            # Shuffle and select 10 random articles to display
            random.shuffle(news)
            selected_news = [{
                'title': article['title'],
                'description': truncate_text(article.get('description', ''), 30),
                'url': article['url'],
                'image_url': article.get('image', '')  # Image URL if available
            } for article in news[:10]]  # Display 10 random articles
            
            if trending_news is not None:
                trending_news = [{
                    'title': article['title'],
                    'description': truncate_text(article.get('description', ''), 30),
                    'url': article['url'],
                    'image_url': article.get('image', '')  # Image URL if available
                } for article in trending_news[:10]]  # Display 10 random articles
            
            # Return rendered template with news and trending news
            return render_template('index.html', news=selected_news, trending_news=trending_news, categories=categories, query=query)
        else:
            # Handle no news available case
            return render_template('index.html', error='Error fetching news. Please try again later.', categories=categories)
    except Exception as e:
        return render_template('index.html', error=f'An error occurred: {e}', categories=categories)

if __name__ == "__main__":
    app.run(debug=True)
