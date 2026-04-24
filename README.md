# BriefD - A News Aggregator Web App

BriefD is a simple Flask-based web application that fetches and displays the latest news from various categories using the Mediastack API. The application allows users to select different news categories and view the latest articles in those categories. It uses a responsive, clean design powered by **Tailwind CSS**.

## Features

- **News Fetching**: Fetches the latest news from the Mediastack API based on user-selected categories.
- **Categories**: Users can choose between multiple categories (e.g., business, sports, technology).
- **Trending News**: Displays trending news articles alongside the selected news.
- **Error Handling**: Displays an error message if there's an issue fetching news from the API.
- **Responsive Design**: The app is fully responsive and works on all screen sizes.

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Frontend**: HTML, CSS (TailwindCSS for styling)
- **API**: Mediastack API for fetching news articles
- **Python Libraries**:
  - `requests`: For making HTTP requests to the Mediastack API
  - `Flask`: For handling web requests and rendering templates
