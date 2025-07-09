# 📈 Binance WebSocket Price Tracker (BTC/ETH) — Flask + PostgreSQL
This project captures **live price updates** for **BTCUSDT** and **ETHUSDT** from Binance using a WebSocket client, stores them with precision in a **PostgreSQL** database, and exposes RESTful APIs to query:
- 🔹 Latest price  
- 🔹 Price at a specific second  
- 🔹 High/low price within a 1-minute interval  

It also includes a **Flask-powered web UI** (`index.html`) for easy testing and visualization.


## 🧱 Folder Structure
binance-price-tracker/
│
├── app.py                  # Flask web server (API + UI rendering)
├── ws_client.py           # Binance WebSocket client (real-time ingestion)
├── db.py                  # DB connection helper
├── requirements.txt       # Python dependencies (optional)
│
├── templates/
│   └── index.html         # Frontend web interface (Flask-rendered)
│
└── venv/                  # Python virtual environment (created locally)

## 🔧 Setup & Installation
### 📦 Step 1: Install PostgreSQL
- Download from: https://www.postgresql.org/download/windows/
- During setup:
  - ✅ Choose a password (e.g., `postgres`)
  - ✅ Install **pgAdmin**
  - ❌ On “StackBuilder” page: Skip or cancel


### 💻 Step 2: Create Database
In **pgAdmin** or `psql`, run:
CREATE DATABASE binance_prices;

Inside that DB, run:
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    price NUMERIC(18,8),
    timestamp TIMESTAMP NOT NULL
);

### 🐍 Step 3: Set Up Python Environment
python -m venv venv
venv\Scripts\activate         # On Windows
# or
source venv/bin/activate     # On Linux/macOS

pip install flask psycopg2-binary websockets
> ✅ Use `pip freeze > requirements.txt` if needed.


## 🧠 Implementation Overview
* **WebSocket Client** (`ws_client.py`):
  Connects to Binance WebSocket for BTC/ETH prices, extracts symbol/price/timestamp, and inserts into PostgreSQL.

* **Database Schema**:
  Stores prices with:
  * `symbol` (e.g., BTCUSDT)
  * `price` (with 8-digit precision)
  * `timestamp` (accurate to the second)

* **Flask App** (`app.py`):
  Exposes 3 APIs and renders the frontend UI.

* **Frontend** (`index.html`):
  Lets users:
  * View latest prices
  * Query a price at a specific time
  * View 1-minute high/low


## ▶️ How to Run the Project
1. **Start WebSocket Price Ingestion**
python ws_client.py
*(Keep this terminal running — it streams data continuously into the DB)*

2. **Start Flask Server**
python app.py

3. **Visit the Web Interface**
Open:
`http://127.0.0.1:5000`



## 🧪 How to Test the System
### ✅ Use the Web UI
Visit: `http://127.0.0.1:5000`
You can:
* Click **Get Latest** ✅
* Choose symbol & time → **Get Price** ✅
* Choose timestamp → **Get High/Low** ✅


### ✅ Use Browser/API Tools (like Postman)
#### 1. 🔹 Latest Prices
GET http://127.0.0.1:5000/latest

#### 2. 🔹 Price at Specific Second (Improved Logic)
GET http://127.0.0.1:5000/price-at-second?symbol=BTCUSDT&timestamp=2025-07-03T08:30:36
> 📌 If no exact timestamp is available, returns the **closest earlier price**.
**Example Response:**
{
  "symbol": "BTCUSDT",
  "timestamp": "2025-07-03T08:30:36",
  "price": "61928.31",
  "actual_timestamp": "2025-07-03T08:30:35.984239"
}
> ⚠️ If no price is found before or at that timestamp, `"price": "N/A"` is returned.

#### 3. 🔹 High/Low in 1-Minute Interval
GET http://127.0.0.1:5000/minmax?symbol=ETHUSDT&timestamp=2025-07-03T08:30
**Example Response:**
{
  "symbol": "ETHUSDT",
  "minute": "2025-07-03T08:30",
  "high": 2611.82,
  "low": 2609.47
}
If no prices were recorded during that minute, high/low will return `null`.


## ✅ What to Expect
| Feature                       | ✅ Status |
| ----------------------------- | --------   |
| Real-time WebSocket ingestion | ✅ Yes    |
| PostgreSQL storage            | ✅ Yes    |
| Flask API with 3 endpoints    | ✅ Yes    |
| Visual HTML testing UI        | ✅ Yes    |
| Handles missing timestamps    | ✅ Yes    |



## 💡 Tech Stack
| Tool       | Purpose                       |
| ---------- | ----------------------------- |
| Python     | Core programming              |
| Flask      | Web framework (UI + API)      |
| WebSockets | Real-time Binance streaming   |
| PostgreSQL | Time-series price storage     |
| pgAdmin    | GUI for PostgreSQL            |
| HTML + JS  | Frontend UI                   |
| psycopg2   | PostgreSQL adapter for Python |
