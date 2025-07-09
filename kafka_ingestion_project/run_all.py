import subprocess
import time
import requests
import sys

def wait_for_flask(url, timeout=30):
    print("[⏳] Waiting for Flask to be ready...")
    for i in range(timeout):
        try:
            res = requests.get(url)
            if res.status_code == 200:
                print("[✅] Flask is ready.")
                return True
        except:
            pass
        time.sleep(1)
    print("[❌] Flask did not start in time.")
    return False

python_exe = sys.executable  # ✅ Use current Python interpreter

print("[🚀] Starting Flask producer...")
flask_proc = subprocess.Popen([python_exe, "app/producer_app.py"])

# Wait for Flask API to be ready
if not wait_for_flask("http://localhost:5000/get_status"):
    print("❌ Exiting: Flask did not respond.")
    flask_proc.terminate()
    exit(1)

print("[🧾] Starting Kafka consumer...")
consumer_proc = subprocess.Popen([python_exe, "app/consumer_app.py"])

# Optional delay
time.sleep(2)

print("[⚡] Starting load test...")
load_test_proc = subprocess.Popen([python_exe, "load_test.py"])
load_test_proc.wait()

print("[✅] Load test finished.")
print("🔁 Press Ctrl+C to stop Flask and Consumer.")

try:
    flask_proc.wait()
    consumer_proc.wait()
except KeyboardInterrupt:
    print("\n[🛑] Terminating...")
    flask_proc.terminate()
    consumer_proc.terminate()
