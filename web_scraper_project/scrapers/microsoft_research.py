import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

class MicrosoftResearchScraper:
    def __init__(self):
        self.base_url = "https://www.microsoft.com/en-us/research/blog/"
        self.data = []
        
    def scrape(self, max_pages=2):
        with sync_playwright() as p:
            # Launch browser with visible window for debugging
            browser = p.chromium.launch(headless=False)
            context = browser.new_context(
                user_agent=HEADERS["User-Agent"],
                viewport={"width": 1280, "height": 800},
                extra_http_headers=HEADERS
            )
            page = context.new_page()
            
            try:
                print("Navigating to Microsoft Research Blog...")
                page.goto(self.base_url, timeout=60000)
                
                # Take screenshot to verify what we're seeing
                page.screenshot(path="data/debug_page.png")
                print("Screenshot saved as debug_page.png")
                
                # Wait for articles to load - using more generic selector
                print("Waiting for content to load...")
                page.wait_for_selector("article, div[class*='post'], div[class*='card']", timeout=15000)
                
                # Get the full page HTML after JavaScript execution
                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Find all article containers - multiple possible selectors
                articles = soup.find_all(['article', 'div'], class_=re.compile(r'post|card|item|article|blog'))
                
                if not articles:
                    print("WARNING: No articles found using CSS selectors. Trying alternative approach...")
                    # Fallback to more generic approach
                    articles = soup.find_all(['article', 'div'], recursive=True)
                    articles = [a for a in articles if a.find('h2') or a.find('h3')]
                
                print(f"Found {len(articles)} potential articles")
                
                for i, article in enumerate(articles, 1):
                    try:
                        # Extract title with multiple fallbacks
                        title_elem = article.find(['h2', 'h3']) or article.find(attrs={'class': re.compile(r'title|heading')})
                        title = title_elem.get_text(strip=True) if title_elem else "No title"
                        
                        # Extract link
                        link = None
                        if title_elem and title_elem.find('a'):
                            link = title_elem.find('a')['href']
                        elif article.find('a', href=True):
                            link = article.find('a')['href']
                        
                        if link and not link.startswith('http'):
                            link = self.base_url + link.lstrip('/')
                        
                        # Extract description
                        desc_elem = article.find(class_=re.compile(r'excerpt|desc|content')) or article.find('p')
                        description = desc_elem.get_text(strip=True) if desc_elem else ""
                        
                        # Extract date
                        date_elem = article.find(class_=re.compile(r'date|time')) or article.find('time')
                        date = date_elem.get_text(strip=True) if date_elem else ""
                        
                        # Only add if we have at least a title
                        if title != "No title":
                            self.data.append({
                                "source": "Microsoft Research Blog",
                                "title": title,
                                "link": link,
                                "description": description,
                                "date": date,
                                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            print(f"  {i}. Added: {title[:60]}...")
                        else:
                            print(f"  {i}. Skipped - no valid title found")
                            
                    except Exception as e:
                        print(f"  {i}. Error processing article: {str(e)}")
                        continue
                
                print(f"\nSuccessfully captured {len(self.data)} articles")
                
            except Exception as e:
                print(f"\nERROR: {str(e)}")
                print("Check debug_page.png to see what the browser loaded")
            finally:
                browser.close()
                
        return self.data
    
    def save_to_json(self, filename="data/microsoft_research_articles.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        print(f"\nData saved to {filename}")
    
    def save_to_csv(self, filename="data/microsoft_research_articles.csv"):
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    print("Starting Microsoft Research Blog Scraper...")
    scraper = MicrosoftResearchScraper()
    data = scraper.scrape(max_pages=1)
    
    if not data:
        print("\nWARNING: No data was scraped. Possible reasons:")
        print("1. The website structure changed - check debug_page.png")
        print("2. Anti-bot measures are blocking the scraper")
        print("3. Network issues prevented loading the page properly")
    else:
        scraper.save_to_json()
        scraper.save_to_csv()
    
    print("\nScraping process completed")