# 📘 Project Summary – Web3 Daily Newsletter Bot

## 🧩 Challenges Faced
1. **Telegram Markdown Parsing Errors (400 Bad Request)**  
   - Telegram's MarkdownV2 format is extremely strict, requiring special characters (e.g., `_`, `-`, `.`, `(`, `)`, `!`) to be escaped properly.
   - Improper escaping resulted in recurring 400 errors even when the newsletter preview looked correct.
   - ✅ *Solution:* Initially tried MarkdownV2 escaping, then opted for **plain text formatting with emoji-based bullet points** for maximum compatibility.

2. **Telegram Message Length Limit (4096 characters)**  
   - When summarizing top 10 articles with full context, Telegram message size exceeded the limit.
   - ✅ *Solution:* Introduced **automatic chunking**, splitting messages into smaller parts without breaking article integrity.

3. **LangChain Agent Latency**  
   - Summarizing articles using LangChain's LLM agents took ~30–60 seconds per batch.
   - ✅ *Solution:* Optimized prompt size and limited to **top 10 articles** to reduce API cost and latency.

4. **Duplicate Article Titles from Multiple Sources**  
   - Same news was often repeated with minor differences across CoinDesk, CoinTelegraph, etc.
   - ✅ *Solution:* Applied **cosine similarity on cleaned titles** to deduplicate articles before summarization.


## 🧱 Architectural Decisions
1. **Modular Design by Responsibility**
   - `scrapers/`: Each news source has its own independent scraper module.
   - `processors/`: Handles deduplication and summarization logic.
   - `newsletter/`: Responsible for message formatting and escaping.
   - `bots/telegram.py`: Interfaces with the Telegram Bot API for message delivery.

2. **Stateless, On-Demand Pipeline**
   - No databases or local storage. Articles are scraped fresh on each run.
   - ✅ *Pros:* Lightweight, simple, and serverless-friendly.
   - ⚠️ *Cons:* No replay or backfill support for true “multi-day” simulation.

3. **Simulated Multi-Day Mode**
   - `scheduler.py` can simulate **two days** by triggering the full pipeline twice.
   - This is a structural simulation—**not based on real date filtering**—because historical article fetching was not implemented due to time constraints.

4. **LangChain + OpenAI**
   - Chosen for flexible summarization using agentic prompt chaining and ease of integration with Pydantic for validation.


## 🔭 Scope for Improvement
**🗃️ Persistent Storage** - Store article metadata to avoid duplicates across days and enablereal multi-day  tracking.                                                                               
**🧠 Smarter Deduplication** - Use semantic embeddings (via FAISS or Chroma) to cluster similar articles effectively.
**📨 Automatic Chunking** - Make message-splitting more intelligent (e.g., split at 5 articles if needed, avoid mid-article breaks).
**📅 Date-Based Filtering** - Scrape based on article publish dates to truly simulate yesterday + today summaries.
**📊 Dashboard Interface** - Use Streamlit or Flask UI to preview, approve, or manually edit newsletters before sending. 
**📂 Historical Archives** - Save past newsletters to a file system or cloud database for backtracking, versioning, or email export. |
**🧪 More LLM Control** - Add custom prompt templates and few-shot examples to improve consistency in summaries. 


## 📌 Conclusion
Despite strict Telegram formatting constraints and the challenge of dealing with LLM latency, the system now:
- ✅ Scrapes 5 top Web3 sources  
- ✅ Deduplicates and summarizes articles  
- ✅ Composes a daily newsletter  
- ✅ Sends it cleanly to Telegram  
- ✅ Simulates 2-day output runs  

The project is **deployment-ready**, modular, and lays a strong foundation for a future production-grade Web3 newsletter automation platform.
