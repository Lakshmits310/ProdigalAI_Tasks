from datetime import datetime, timedelta
import time

from scrapers.coindesk import CoinDeskScraper
from scrapers.cointelegraph import CoinTelegraphScraper
from scrapers.decrypt import DecryptScraper
from scrapers.theblock import TheBlockScraper
from scrapers.bankless import BanklessScraper

from processors.deduplicator import Deduplicator
from processors.summarizer import Summarizer
from newsletter.composer import NewsletterComposer
from bots.telegram import TelegramBot

def run_daily_newsletter():
    # Initialize components
    scrapers = [
        CoinDeskScraper(),
        CoinTelegraphScraper(),
        DecryptScraper(),
        TheBlockScraper(),
        BanklessScraper()
    ]
    deduplicator = Deduplicator()
    summarizer = Summarizer()
    composer = NewsletterComposer()
    bot = TelegramBot()

    all_articles = []

    # Collect top 2 articles per source
    for scraper in scrapers:
        try:
            print(f"🔍 Scraping from {scraper.__class__.__name__}...")
            articles = scraper.scrape()
            top_articles = articles[:2] if len(articles) >= 2 else articles
            print(f"✅ Collected {len(top_articles)} articles from {scraper.__class__.__name__}")
            all_articles.extend(top_articles)
        except Exception as e:
            print(f"❌ Error scraping {scraper.__class__.__name__}: {e}")

    print(f"\n🔎 Total collected articles before deduplication: {len(all_articles)}")

    # Deduplicate
    unique_articles = deduplicator.deduplicate(all_articles)
    print(f"🧹 Unique articles after deduplication: {len(unique_articles)}")

    if not unique_articles:
        print("❌ No unique articles found. Skipping newsletter.")
        return

    # Summarize
    summarized_articles = summarizer.summarize_articles(unique_articles)
    print(f"🧠 Summarized {len(summarized_articles)} articles")

    # Compose
    newsletter = composer.compose(summarized_articles)
    print("\n📨 Newsletter Preview:\n")
    print(newsletter[:800], "...\n")  # Optional preview

    # Send
    sent = bot.send_message(newsletter)
    print("✅ Sent!" if sent else "❌ Failed to send.")

if __name__ == "__main__":
    run_daily_newsletter()
