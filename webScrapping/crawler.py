import requests
from bs4 import BeautifulSoup
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import sqlite3
import random
from queue import Queue

class Crawler:
    def __init__(self, start_url, max_pages, user_id, max_threads=10, batch_size=100):
        self.start_url = start_url
        self.max_pages = max_pages
        self.user_id = user_id
        self.crawled_data = []
        self.visited_urls = set()
        self.is_running = False
        self.max_threads = max_threads
        self.batch_size = batch_size
        self.session = requests.Session()  # Use session to persist connections

    def start(self):
        self.is_running = True
        self.crawl()
        self.save_results()

    def crawl(self):
        to_visit = Queue()
        to_visit.put(self.start_url)
        visited_urls = set()

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            while not to_visit.empty() and len(self.crawled_data) < self.max_pages:
                url = to_visit.get()
                if url not in visited_urls:
                    visited_urls.add(url)
                    executor.submit(self._crawl_page, url, to_visit)

            executor.shutdown(wait=True)

    def _crawl_page(self, url, to_visit):
        retries = 5
        for _ in range(retries):
            try:
                response = self.session.get(url)  # Use session for requests
                if response.status_code == 200:
                    self._process_response(response, to_visit)
                    return
                elif response.status_code == 429:
                    print("Rate limit exceeded. Retrying...")
                    time.sleep(2 ** _ + random.uniform(1, 3))  # Exponential backoff
                else:
                    print(f"Failed to retrieve {url}, status code: {response.status_code}")
                    return
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(random.uniform(1, 3))  # Random delay in case of errors

        time.sleep(random.uniform(1, 3))  # Random delay between requests

    def _process_response(self, response, to_visit):
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'
        print(f"Page title: {title}")
        self.crawled_data.append({'url': response.url, 'title': title})

        # Find and process links to crawl next
        for link in soup.find_all('a', href=True):
            next_url = link['href']
            if next_url.startswith('http') and next_url not in self.visited_urls:
                to_visit.put(next_url)

    def save_results(self):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        data_to_insert = []

        for data in self.crawled_data:
            data_to_insert.append((self.user_id, data['url'], data['title']))

            # If batch size is reached, commit data
            if len(data_to_insert) >= self.batch_size:
                cursor.executemany('INSERT INTO crawled_results (user_id, url, title) VALUES (?, ?, ?)', data_to_insert)
                conn.commit()
                data_to_insert = []  # Clear the batch

        # Insert any remaining data
        if data_to_insert:
            cursor.executemany('INSERT INTO crawled_results (user_id, url, title) VALUES (?, ?, ?)', data_to_insert)
            conn.commit()

        conn.close()
        print("Results saved to the database.")

    def get_results(self):
        return self.crawled_data

    def stop(self):
        print("Stopping the crawler.")
        self.is_running = False  # Implement any logic necessary to stop the crawler if needed

