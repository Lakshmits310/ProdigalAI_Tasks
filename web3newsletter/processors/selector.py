from typing import List, Dict
from config import TOTAL_ARTICLES_TO_SELECT, PUBLICATIONS

class ArticleSelector:
    def select_top_articles(self, articles: List[Dict]) -> List[Dict]:
        """Select top articles ensuring at least one from each publication"""
        selected = []
        publications = list(PUBLICATIONS.keys())
        
        # First pass: Ensure at least one from each publication
        for pub in publications:
            pub_articles = [a for a in articles if a['source'] == pub]
            if pub_articles:
                selected.append(pub_articles[0])
        
        # Second pass: Fill remaining slots with most recent articles
        remaining_slots = TOTAL_ARTICLES_TO_SELECT - len(selected)
        if remaining_slots > 0:
            # Get articles not already selected, sorted by date (newest first)
            other_articles = [
                a for a in articles 
                if a not in selected
            ]
            # Sort by date (simplified - in production would parse dates properly)
            other_articles_sorted = sorted(
                other_articles,
                key=lambda x: x['date'],
                reverse=True
            )
            selected.extend(other_articles_sorted[:remaining_slots])
        
        return selected[:TOTAL_ARTICLES_TO_SELECT]