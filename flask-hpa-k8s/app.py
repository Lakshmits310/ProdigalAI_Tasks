from flask import Flask
import time
import threading

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Flask! Visit /load to simulate CPU load."

@app.route('/load')
def load():
    def burn():
        t_end = time.time() + 15
        while time.time() < t_end:
            pass  # Busy-wait for 10s

    threads = []
    for _ in range(40):  # 10 threads
        thread = threading.Thread(target=burn)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return "CPU load simulated for 15 seconds using 40 threads!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
