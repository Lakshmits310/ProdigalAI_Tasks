## 📌 Article + Scheme Scraper & Summary Report
This project involves scraping structured information from two different web sources:
- *Microsoft Research Blog* – a dynamically loaded site with "Load More" functionality.
- *MyScheme Portal* – a statically paginated government scheme listing site.
The goal was to collect titles, descriptions, and links from each, save the data in JSON/CSV formats, and produce a technical report on scraper performance and design.


## 🧱 Architectural Decisions
### 1. Technology Stack
- *Python + Playwright*: Chosen for its modern headless browser automation, capable of handling JavaScript-heavy sites.
- *pandas*: For CSV exports and tabular manipulation.
- *JSON module*: To store structured data outputs.
- *Folder Structure*:

### 2. Data Pipeline
- Scraping scripts extract page elements using CSS selectors.
- "Load more" or pagination is simulated using Playwright actions (scrolling/clicking).
- After collection, data is written into .json and .csv formats in data/ folders.


## ⚠ Challenges Faced
### 🔹 Microsoft Research Blog
- *Dynamic loading behavior*: Articles appear only after clicking "Load More" or scrolling.
- *Scroll detection*: Required delays and retry logic to ensure full content was loaded.
- *Missing selectors*: Some articles had inconsistent HTML tags for summaries.

### 🔹 MyScheme Portal
- *Pagination*: Each page had a new URL but predictable structure.
- *Uniform layout*: Made extraction straightforward, but small delays were needed to avoid request throttling.

### 🔹 General Issues
- *Playwright install quirks*: OS-level dependencies and browser downloads were tricky at first.
- *Error handling*: Needed try-except blocks to handle page loading failures and element-not-found errors.
- *Consistency*: Some entries on both sites lacked descriptions or links, requiring conditional logic.


## 🔍 Data Completeness Evaluation

| Site                  | Data Fields        | Completeness (%) | Comments                                    |
|-----------------------|--------------------|------------------|---------------------------------------------|
| MyScheme Portal       | Title, Link, Desc  | ~100%            | All pages covered via pagination            |
| Microsoft Research    | Title, Link, Desc  | ~85–90%          | Limited by number of "Load More" clicks and | 
|                       |                    |                  | lazy-loaded articles                        |


## 🚀 Scope for Improvement
### ✅ Short-Term
- Use *proxy rotation* to simulate organic user behavior and avoid any future IP blocking.
- Add *command-line arguments* for configurable output paths or page limits.

### ✅ Long-Term
- Integrate *SQLite/PostgreSQL* to persist scraped data instead of just flat files.
- Build a *Flask dashboard* to visualize scheme/article summaries.
- Add *NLP summarization* for long descriptions using Hugging Face or spaCy pipelines.

