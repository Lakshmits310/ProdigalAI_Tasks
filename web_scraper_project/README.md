## 🕸️ Web Scraper Dashboard
A Flask-based web application that scrapes content from:
* [Microsoft Research Blog](https://www.microsoft.com/en-us/research/blog/)
* [MyScheme Portal](https://www.myscheme.gov.in)
It then displays summaries, charts, tables, and allows downloading the scraped data and report.


## 📁 Project Structure
web_scraper_project/
│
├── app.py                           # Main Flask app
├── requirements.txt                 # Python dependencies
├── templates/
│   └── index.html                   # Web UI (dashboard)
├── static/
│   └── styles.css                   # CSS styling
│
├── scrapers/
│   ├── __init__.py                  # DataHandler (main logic)
│   ├── microsoft_research.py       # Microsoft scraper
│   └── myscheme.py                 # MyScheme scraper
│
├── data/                            # Auto-created during scraping
│   ├── combined_data.json
│   ├── combined_data.csv
│   ├── scraping_report.json
│   ├── microsoft/
│   │   ├── microsoft_data.json
│   │   └── microsoft_data.csv
│   └── myscheme/
│       ├── myscheme_data.json
│       └── myscheme_data.csv


## 🔧 Setup Instructions
1. **Install Python 3.8+**

2. **Clone the Repository**
   git clone https://github.com/yourusername/web_scraper_project.git
   cd web_scraper_project

3. **Create a Virtual Environment (Optional)**
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate

4. **Install Required Packages**
   pip install -r requirements.txt

5. **Install Playwright Browsers (Once)**
   playwright install


## 🚀 Running the App
python app.py
Visit **[http://localhost:5000](http://localhost:5000)** in your browser.


## 🧠 Features
* ✅ Scrapes Microsoft Research Blog and MyScheme Portal
* ✅ Saves results to:
  * `data/combined_data.json`
  * `data/microsoft/microsoft_data.json`
  * `data/myscheme/myscheme_data.json`

* ✅ Generates `scraping_report.json` summarizing:
  * Total records
  * Challenges encountered
  * Data completeness

* ✅ Interactive Dashboard:
  * Run scraper
  * View summary stats and charts
  * Browse data in table
  * Download JSON/CSV
  * View report


## 🖼️ Dashboard UI Features
| Feature         | Description                              |
| --------------- | ---------------------------------------- |
| **Run Scraper** | Triggers scraping of both sources        |
| **Load Data**   | Loads the table and stats after scraping |
| **Download**    | Get combined data as JSON or CSV         |
| **View Report** | See scraping insights and challenges     |


## 📌 What to Expect
| Source          | Expectation                                  |
| --------------- | -------------------------------------------- |
| Microsoft Blog  | \~30+ articles parsed from latest blog posts |
| MyScheme Portal | \~20–30 schemes for keyword `health`         |
| Output Folders  | Auto-created under `data/`                   |
| Browser Windows | Will briefly open for scraping (debug mode)  |


## ⚠️ Known Issues
* ❌ Playwright may timeout if internet is slow or content fails to load
* ⚠️ Ensure Chrome is installed and available for Playwright
* ❗ If "No data" appears:
  * Check the `data/` folder
  * Look at `data/*.png` debug screenshots
  * Run scraper again
