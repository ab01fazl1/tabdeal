# Replace with your actual API endpoint and request data
import requests
import threading
import time

url = "http://127.0.0.1:8000/api/v1/transactions/"
REQUEST_DATA = {"from_account_id": 2, "phone_number": "11111111111", "amount":1}

# Function to send a POST request
def send_post_request(url):
    response = requests.post(url, data=REQUEST_DATA)
    print(response.status_code)

# Function to send multiple POST requests using multi-threading
def main():
    urls = ["http://127.0.0.1:8000/api/v1/transactions/"] * 100  # Replace with your API endpoint
    threads = []

    start_time = time.time()

    for url in urls:
        thread = threading.Thread(target=send_post_request, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(time.time() - start_time)

if __name__ == "__main__":
    main()
