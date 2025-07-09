import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time

URL = "http://localhost:5000/register_event"

def send_event(i):
    data = {"event_id": i, "event_type": "click"}
    try:
        response = requests.post(URL, json=data, timeout=2)
        return response.status_code
    except Exception as e:
        return str(e)

start = time.time()

with ThreadPoolExecutor(max_workers=100) as executor:
    results = list(executor.map(send_event, range(10000)))

end = time.time()

print(f"Sent 10,000 requests in {end - start:.2f} seconds.")
success_count = sum(1 for r in results if r == 200)
print(f"Success: {success_count}, Failures: {10000 - success_count}")
