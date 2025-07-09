# 📰 Web3 Daily Newsletter Bot
An **automated multi-agent system** that scrapes news from top Web3 sources, summarizes them using LLM agents, and sends a **daily digest to Telegram**.


## 📌 Objective
Automate the process of gathering, deduplicating, summarizing, and broadcasting the **top 10 Web3 articles daily**.

## 📁 Project Structure
web3newsletter/
├── bots/
│   └── telegram.py              # Telegram bot integration and message sending logic
│
├── newsletter/
│   ├── composer.py              # Formats the newsletter content (header, body, footer)
│   └── templates.py             # Defines header, body, and footer templates for the newsletter
│
├── processors/
│   ├── deduplicator.py          # Removes similar or duplicate articles
│   └── summarizer.py            # Summarizes articles using LangChain agent
│
├── scrapers/
│   ├── __init__.py
│   ├── bankless.py              # Scraper for Bankless
│   ├── coindesk.py              # Scraper for CoinDesk
│   ├── cointelegraph.py         # Scraper for CoinTelegraph
│   ├── decrypt.py               # Scraper for Decrypt
│   └── theblock.py              # Scraper for The Block
│   └──base_scraper.py           # Abstract base class for consistent scraper structure
|
├── scheduler.py                 # Runs the end-to-end newsletter automation
├── test_one_source.py          # Testing script for single source
├── config.py                    # Stores API tokens and configuration constants
├── README.md                    # Project overview and instructions
└── SUMMARY.md                   # Challenges, architecture decisions, improvements
└── requirements.txt



## 🧠 Features
✅ Scrapes latest articles from:
- CoinDesk  
- CoinTelegraph  
- Decrypt  
- The Block  
- Bankless  

✅ Deduplicates similar articles using cosine similarity on titles  
✅ Summarizes top 10 articles using **LangChain LLM agent**  
✅ Formats newsletter (Header, Body, Footer)  
✅ Sends formatted digest to a **Telegram group**  
✅ Optionally simulates **2 days of newsletters**


## 📦 Tech Stack
- Python 3.8+
- LangChain agents (OpenAI/GPT-based)
- Pydantic for validation
- Requests + BeautifulSoup for scraping
- Telegram Bot API
- Optional: VectorDB (for future memory / clustering)


## 🔧 Installation
git clone https://github.com/yourusername/web3newsletter.git
cd web3newsletter
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate
pip install -r requirements.txt

> 💡 Make sure you add your API keys in `config.py`:
TELEGRAM_TOKEN = "your_bot_token_here"
TELEGRAM_CHAT_ID = "your_group_id_here"


## 🚀 Running the Bot
### 🔹 1. Run Once (Today's News)
python test_one_source.py
> Scrapes one source (adjust as necessary) and pushes to Telegram.

Or for all 5 sources:
python scheduler.py

### 🔹 2. Simulate Two Days
# scheduler.py
python scheduler.py
This runs the same pipeline twice in a row (2 seconds apart), simulating two newsletter days.
Note: Currently, this uses **the same day's feed twice**, as historical news fetching is not implemented.

## 📬 Telegram Demo
You can join the test group here:
👉 [Telegram Group Invite](https://t.me/+FOG_ggda6xMyYzc1)


## 🧪 Deliverables
* ✅ Scraper pipelines for 5 sources
* ✅ Deduplication logic
* ✅ LangChain-based summarizer
* ✅ Markdown-safe composer
* ✅ Telegram push integration
* ✅ `scheduler.py` for 1-day simulation
* ✅ Newsletter sample output (see Telegram group)
* ✅ README with usage


## 📝 To-Do / Future Enhancements
* Store historical articles to JSON for real 2-day simulation
* Split newsletter automatically into chunks if too long
* Add UI/streamlit interface for manual preview
* Use VectorDB to cluster similar news intelligently
