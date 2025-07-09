import requests
import threading
import time

URL = "http://127.0.0.1:58640/load"  # or use `minikube service flask-service --url`

def hit_load():
    try:
        r = requests.get(URL)
        print(r.text)
    except Exception as e:
        print("Request failed:", e)

threads = []
for _ in range(50):  # Launch 50 simultaneous requests
    t = threading.Thread(target=hit_load)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("Heavy Load sent!")
