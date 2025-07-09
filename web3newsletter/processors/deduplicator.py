from typing import List, Dict
import re

class Deduplicator:
    @staticmethod
    def normalize_title(title: str) -> str:
        """Normalize titles for comparison"""
        title = title.lower()
        title = re.sub(r'[^\w\s]', '', title)  # Remove punctuation
        return title.strip()

    def deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on title similarity"""
        seen_titles = set()
        unique_articles = []
        
        for article in articles:
            norm_title = self.normalize_title(article['title'])
            
            # Check if a similar title already exists
            is_duplicate = False
            for seen_title in seen_titles:
                if self.is_similar(norm_title, seen_title):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_titles.add(norm_title)
                unique_articles.append(article)
                
        return unique_articles

    def is_similar(self, title1: str, title2: str, threshold: float = 0.8) -> bool:
        """Basic similarity check between titles"""
        words1 = set(title1.split())
        words2 = set(title2.split())
        intersection = words1 & words2
        similarity = len(intersection) / max(len(words1), len(words2))
        return similarity >= threshold