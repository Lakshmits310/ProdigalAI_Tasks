from flask import Flask, jsonify, request, render_template
from db import get_connection
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/latest")
def latest():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p1.symbol, p1.price, p1.timestamp
        FROM prices p1
        JOIN (
            SELECT symbol, MAX(timestamp) AS latest_ts
            FROM prices
            GROUP BY symbol
        ) p2 ON p1.symbol = p2.symbol AND p1.timestamp = p2.latest_ts
    """)
    rows = cur.fetchall()
    conn.close()
    result = [[r[0], str(r[1]), r[2].strftime("%a, %d %b %Y %H:%M:%S GMT")] for r in rows]
    return jsonify(result)

@app.route("/price-at-second")
def price_at_second():
    symbol = request.args.get("symbol")
    ts = request.args.get("timestamp")
    try:
        ts_obj = datetime.fromisoformat(ts)
    except:
        return jsonify({"error": "Invalid timestamp format"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT price, timestamp 
        FROM prices 
        WHERE symbol = %s AND timestamp <= %s 
        ORDER BY timestamp DESC 
        LIMIT 1
    """, (symbol, ts_obj))
    row = cur.fetchone()
    conn.close()

    return jsonify({
        "symbol": symbol,
        "timestamp": ts,
        "price": str(row[0]) if row else "N/A",
        "actual_timestamp": row[1].isoformat() if row else None
    })

@app.route("/minmax")
def min_max():
    symbol = request.args.get("symbol")
    ts = request.args.get("timestamp")
    try:
        ts_obj = datetime.fromisoformat(ts)
        minute = ts_obj.replace(second=0, microsecond=0)
    except:
        return jsonify({"error": "Invalid timestamp format"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(price), MIN(price)
        FROM prices
        WHERE symbol = %s AND DATE_TRUNC('minute', timestamp) = %s
    """, (symbol, minute))
    row = cur.fetchone()
    conn.close()

    return jsonify({
        "symbol": symbol,
        "minute": ts,
        "high": float(row[0]) if row[0] else None,
        "low": float(row[1]) if row[1] else None
    })

@app.route("/chart-data")
def chart_data():
    symbol = request.args.get("symbol", "BTCUSDT")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT timestamp, price
        FROM prices
        WHERE symbol = %s
        ORDER BY timestamp DESC
        LIMIT 30
    """, (symbol,))
    rows = cur.fetchall()
    conn.close()

    data = {
        "labels": [row[0].strftime("%H:%M:%S") for row in rows[::-1]],
        "prices": [float(row[1]) for row in rows[::-1]]
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
