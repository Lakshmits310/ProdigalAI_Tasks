import xml.etree.ElementTree as ET
from .base_scraper import BaseScraper
from datetime import datetime
from typing import List, Dict

class CoinDeskScraper(BaseScraper):
    def __init__(self):
        super().__init__("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/")

    def parse_articles(self, xml_content: str) -> List[Dict]:
        articles = []
        try:
            root = ET.fromstring(xml_content)
            for item in root.findall(".//item")[:10]:
                title = item.findtext("title", "").strip()
                link = item.findtext("link", "").strip()
                description = item.findtext("description", "").strip()
                pub_date = item.findtext("pubDate", "").strip()

                articles.append({
                    "title": title,
                    "summary": description,
                    "url": link,
                    "date": pub_date,
                    "source": self.source_name
                })
        except Exception as e:
            print(f"CoinDesk parsing failed: {e}")
        return articles
