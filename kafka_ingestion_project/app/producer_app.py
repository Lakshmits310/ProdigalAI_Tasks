from flask import Flask, request, jsonify, render_template
from confluent_kafka import Producer
from datetime import datetime
import json

app = Flask(__name__)

# Kafka configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092'
}
producer = Producer(producer_config)
TOPIC = "events_topic"

# ✅ Delivery report callback
def delivery_report(err, msg):
    if err is not None:
        print(f"[❌ ERROR] Delivery failed: {err}")
    else:
        print(f"[✅ OK] Message delivered to {msg.topic()} [{msg.partition()}]")

# ✅ Home route to render HTML form
@app.route('/')
def home():
    return render_template("index.html")

# ✅ Register Event (handles both JSON & HTML form)
@app.route('/register_event', methods=['POST'])
def register_event():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = {
                "id": request.form.get("id"),
                "name": request.form.get("name"),
                "action": request.form.get("action"),
                "notes": request.form.get("notes"),
                "timestamp": datetime.now().isoformat()
            }

        message = json.dumps(data)
        producer.produce(TOPIC, message.encode('utf-8'), callback=delivery_report)
        producer.flush()

        if request.is_json:
            return jsonify({"status": "Event registered successfully!"}), 200
        else:
            return render_template("index.html", msg="✅ Event registered successfully!")

    except Exception as e:
        print("Error:", e)
        if request.is_json:
            return jsonify({"error": str(e)}), 500
        else:
            return render_template("index.html", msg=f"❌ Error: {e}")

# ✅ Health Check Endpoint
@app.route('/get_status', methods=['GET'])
def get_status():
    return jsonify({"status": "API working, Kafka connected!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
