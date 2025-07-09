import xml.etree.ElementTree as ET
from .base_scraper import BaseScraper
from typing import List, Dict

class DecryptScraper(BaseScraper):
    def __init__(self):
        super().__init__("Decrypt", "https://decrypt.co/feed")

    def parse_articles(self, xml_content: str) -> List[Dict]:
        articles = []
        try:
            root = ET.fromstring(xml_content)
            for item in root.findall(".//item")[:5]:
                title = item.findtext("title", "").strip()
                link = item.findtext("link", "").strip()
                summary = item.findtext("description", "").strip()
                pub_date = item.findtext("pubDate", "").strip()

                articles.append({
                    "title": title,
                    "summary": summary,
                    "url": link,
                    "date": pub_date,
                    "source": self.source_name
                })
        except Exception as e:
            print(f"Decrypt parsing failed: {e}")
        return articles
