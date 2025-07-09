from typing import List, Dict
from datetime import datetime

class NewsletterComposer:
    def compose(self, articles: List[Dict]) -> str:
        date_str = datetime.now().strftime("%B %d, %Y")
        
        header = f"🚀 Web3 Daily Newsletter - {date_str} 🚀\n\nHere are today’s top Web3 news stories:\n\n"
        body = ""

        for idx, article in enumerate(articles, start=1):
            body += (
                f"📰 {idx}. {article['title']} ({article['source']})\n"
                f"{article['summary']}\n"
                f"🔗 {article['url']}\n\n"
            )

        footer = (
            "📬 Stay informed! This newsletter is automatically generated daily.\n"
            "Sources: CoinDesk, CoinTelegraph, Decrypt, The Block, Bankless"
        )

        return header + body + footer