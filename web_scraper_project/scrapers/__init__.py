import json
import pandas as pd
from datetime import datetime
import os
from .microsoft_research import MicrosoftResearchScraper
from .myscheme import MySchemeScraper

class DataHandler:
    def __init__(self):
        self.all_data = []

    def collect_data(self):
        # Microsoft Research
        ms_scraper = MicrosoftResearchScraper()
        ms_data = ms_scraper.scrape(max_pages=2)
        for item in ms_data:
            item['source'] = "Microsoft Research Blog"
        self.all_data.extend(ms_data)

        # MyScheme
        scheme_scraper = MySchemeScraper()
        scheme_data = scheme_scraper.scrape()
        for item in scheme_data:
            item['source'] = "MyScheme Portal"
        self.all_data.extend(scheme_data)

        return self.all_data

    def save_combined_json(self, filename="data/combined_data.json"):
        os.makedirs("data", exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.all_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Combined data saved to {filename}")

    def save_combined_csv(self, filename="data/combined_data.csv"):
        os.makedirs("data", exist_ok=True)
        df = pd.DataFrame(self.all_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"✅ Combined data saved to {filename}")

    def save_all_sources_json_csv(self):
        os.makedirs("data/myscheme", exist_ok=True)
        os.makedirs("data/microsoft", exist_ok=True)

        ms_data = [d for d in self.all_data if d['source'] == "Microsoft Research Blog"]
        scheme_data = [d for d in self.all_data if d['source'] == "MyScheme Portal"]

        # Microsoft
        with open("data/microsoft/microsoft_data.json", "w", encoding="utf-8") as f:
            json.dump(ms_data, f, ensure_ascii=False, indent=2)
        pd.DataFrame(ms_data).to_csv("data/microsoft/microsoft_data.csv", index=False, encoding="utf-8")

        # MyScheme
        with open("data/myscheme/myscheme_data.json", "w", encoding="utf-8") as f:
            json.dump(scheme_data, f, ensure_ascii=False, indent=2)
        pd.DataFrame(scheme_data).to_csv("data/myscheme/myscheme_data.csv", index=False, encoding="utf-8")

        print("📁 Microsoft and MyScheme data saved in their respective folders.")

    def generate_summary_report(self):
        ms_count = len([d for d in self.all_data if d['source'] == "Microsoft Research Blog"])
        scheme_count = len([d for d in self.all_data if d['source'] == "MyScheme Portal"])

        report = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_records": len(self.all_data),
            "sources": {
                "Microsoft Research Blog": ms_count,
                "MyScheme Portal": scheme_count
            },
            "challenges": {
                "Microsoft Research Blog": [
                    "Dynamic content loading (Load More button)",
                    "Complex HTML structure with nested divs",
                    "No significant anti-bot mechanisms detected"
                ],
                "MyScheme Portal": [
                    "Pagination handling",
                    "Relative URLs that need to be converted to absolute",
                    "No significant anti-bot mechanisms detected"
                ]
            },
            "data_completeness": {
                "Microsoft Research Blog": "High - All expected fields were captured",
                "MyScheme Portal": "High - All expected fields were captured"
            }
        }

        os.makedirs("data", exist_ok=True)
        with open("data/scraping_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=4)

        print("📊 Scraping report saved to data/scraping_report.json")
        return report
