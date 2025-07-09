from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import json
import csv
import os
import time

class MySchemeScraper:
    def __init__(self):
        self.base_url = "https://www.myscheme.gov.in/search"
        self.output_json = "data/myscheme_data.json"
        self.output_csv = "data/myscheme_data.csv"
        self.data = []

    def scrape(self, keyword="health", max_pages=None):
        with sync_playwright() as p:
            print("🚀 Starting MyScheme Scraper...")
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1366, "height": 768})
            page = context.new_page()

            print("🌐 Navigating to search page...")
            page.goto(self.base_url, timeout=60000)
            time.sleep(3)

            try:
                try:
                    acc_btn = page.locator("button[aria-label='Accessibility Options']")
                    if acc_btn.is_visible():
                        acc_btn.click()
                        time.sleep(1)
                except:
                    pass

                print(f"🔎 Typing search keyword: {keyword}")
                search_input = page.locator("input[placeholder='Search']")
                search_input.wait_for(timeout=30000)
                search_input.fill(keyword)
                search_input.press("Enter")
                time.sleep(3)

                card_selector = "div[class*='rounded-xl'][class*='shadow-md']"
                page.wait_for_selector(card_selector, timeout=30000)
                time.sleep(2)

                html = page.content()
                os.makedirs("data", exist_ok=True)
                with open("data/myscheme_debug.html", "w", encoding="utf-8") as f:
                    f.write(html)

                soup = BeautifulSoup(html, "html.parser")
                cards = soup.select(card_selector)

                for card in cards:
                    title_elem = card.select_one("h2, h3")
                    title = title_elem.get_text(strip=True) if title_elem else ""

                    link_elem = card.find("a", href=True)
                    link = "https://www.myscheme.gov.in" + link_elem['href'] if link_elem else ""

                    desc_elem = card.select_one("span.mt-3")
                    description = desc_elem.get_text(" ", strip=True) if desc_elem else ""

                    ministry_elem = card.select_one("h2 + h2")
                    ministry = ministry_elem.get_text(strip=True) if ministry_elem else ""

                    if title:
                        self.data.append({
                            "title": title,
                            "link": link,
                            "description": description,
                            "ministry": ministry,
                            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "source": "MyScheme Portal"
                        })

            except Exception as e:
                print(f"❌ ERROR: {e}")
                page.screenshot(path="data/myscheme_error.png")

            browser.close()

        print(f"\n✅ Scraped {len(self.data)} schemes.")
        return self.data
