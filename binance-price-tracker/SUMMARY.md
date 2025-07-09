## 🧩Binance WebSocket Price Precision Capture (BTC/ETH)  
Consume live price updates from Binance WebSocket for BTC/USDT and ETH/USDT, and store them with precise timestamps and float accuracy for real-time and historical analysis.


## 🏗 Architectural Decisions
### ✅ Data Source
- *Binance WebSocket API* used to consume real-time trade data for BTCUSDT and ETHUSDT.
- Subscribed to the trade stream (<symbol>@trade) to ensure timely and frequent price updates.

### ✅ Technology Stack
- *Language:* Python (for simplicity and speed of development)
- *Database:* PostgreSQL (chosen for its support for time-series operations and precision in numeric types)

### ✅ WebSocket Client
- Implemented using websockets or websocket-client module
- Listens to multi-millisecond trade events for BTC and ETH
- Each message includes:
  - symbol (e.g., BTCUSDT)
  - price (high-precision float)
  - timestamp (converted from Binance's epoch milliseconds)

### ✅ Database Schema
CREATE TABLE prices (
  timestamp TIMESTAMPTZ NOT NULL,
  symbol TEXT NOT NULL,
  price NUMERIC(18, 8) NOT NULL,
  PRIMARY KEY (timestamp, symbol)
);

	•	Primary key prevents duplicate entries at the same timestamp per symbol.
	•	NUMERIC(18,8) ensures float precision for price storage.
	•	Timezone-aware timestamps used for accurate historical queries.

### ✅ Key Query Capabilities
	1.	Latest Price for a Symbol
SELECT * FROM prices
WHERE symbol = 'BTCUSDT'
ORDER BY timestamp DESC
LIMIT 1;

	2.	Price at a Specific Second
SELECT * FROM prices
WHERE symbol = 'ETHUSDT'
AND DATE_TRUNC('second', timestamp) = 'YYYY-MM-DD HH:MM:SS+00';


	3.	Min/Max in a 1-Min Interval
SELECT MIN(price), MAX(price)
FROM prices
WHERE symbol = 'BTCUSDT'
AND timestamp BETWEEN 'start_time' AND 'end_time';

### ✅ Challenges Faced
	•	High-Frequency Ingestion:
	•	Binance sends multiple updates per second per symbol. Ensuring all are captured without missing data required efficient async processing.
	•	DB Write Performance:
	•	Continuous insertions could cause I/O blocking. Considered batching or using an asynchronous queue, but opted for simple, frequent inserts given scope.
	•	Precision Handling:
	•	Python float and PostgreSQL NUMERIC(18, 8) used carefully to avoid rounding errors or data truncation.
	•	Time Sync:
	•	Converted Binance-provided timestamps to UTC-aware datetime objects to allow consistent querying.
	•	WebSocket Reconnection:
	•	Implemented basic retry/reconnect logic to resume data stream on connection loss.

### ✅ Scope for Improvement
	•	Batch Insert Optimization:
	•	Currently, inserts are row-by-row. Switching to batch inserts or using COPY for large volume ingestion can significantly boost write throughput.
	•	Use of InfluxDB:
	•	InfluxDB, being a time-series database, can further optimize querying and compression of time-bound data, especially for longer-term retention.
	•	Indexing Enhancements:
	•	Add indexes on symbol, timestamp to accelerate queries at scale.
	•	Real-Time Dashboard:
	•	Add a small dashboard using Flask + Plotly/Dash to visualize live price trends, min/max, and deltas.
	•	Error Handling & Logging:
	•	Extend retry logic and add better logging (e.g., dropped messages, lag warnings).

### ✅ Status
	•	Live Binance WebSocket client implemented
	•	Real-time multi-pair price ingestion tested
	•	PostgreSQL schema created and validated
	•	Query features demonstrated with working SQL