import requests
from typing import List, Dict

class BaseScraper:
    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_content(self, url: str) -> str:
        response = requests.get(url, headers=self.headers, timeout=40)
        response.raise_for_status()
        return response.text

    def parse_articles(self, raw_content: str) -> List[Dict]:
        raise NotImplementedError("Each scraper must implement its own parse_articles method")

    def scrape(self) -> List[Dict]:
        try:
            content = self.fetch_content(self.base_url)
            articles = self.parse_articles(content)
            return articles[:5]  # Top 5 articles
        except Exception as e:
            print(f"Error scraping {self.source_name}: {e}")
            return []
