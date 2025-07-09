from scrapers.theblock import TheBlockScraper
from processors.deduplicator import Deduplicator
from processors.summarizer import Summarizer
from newsletter.composer import NewsletterComposer
from bots.telegram import TelegramBot
import time

def test_one_source():
    scraper = TheBlockScraper()
    deduplicator = Deduplicator()
    summarizer = Summarizer()
    composer = NewsletterComposer()
    bot = TelegramBot()
    
    print("📡 Scraping CoinDesk...")
    articles = scraper.scrape()
    print(f"✅ Fetched {len(articles)} articles.")
    
    if not articles:
        print("❌ No articles found. Exiting.")
        return
    
    unique_articles = deduplicator.deduplicate(articles)
    
    print("🧠 Summarizing top article...")
    start = time.time()
    summarized_articles = summarizer.summarize_articles(unique_articles[:1])
    print(f"🕒 Time taken: {time.time() - start:.2f}s")
    print("📝 Summarized Articles:")
    for idx, summary in enumerate(summarized_articles, 1):
        print(f"{idx}. {summary}\n")
    
    newsletter = composer.compose(summarized_articles)
    
    print("📨 Newsletter Preview:")
    print(newsletter)
    print("Length:", len(newsletter))

    success = bot.send_message(newsletter)
    print("✅ Sent!" if success else "❌ Failed to send.")

if __name__ == "__main__":
    test_one_source()
