from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from collections import deque
import re

app = Flask(__name__)

def fetch_page(url, timeout=10):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; PythonBot/1.0)"}
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.RequestException as e:
        return None

def extract_important_text(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Remove unwanted elements
    for script_or_style in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form', 'iframe', 'noscript']):
        script_or_style.decompose()

    title = soup.find('h1') or soup.title or "No Title"
    title_text = title.get_text().strip() if hasattr(title, 'get_text') else str(title)

    # Extract important textual elements
    content = ' '.join(tag.get_text(separator=' ', strip=True)
                       for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'figcaption', 'code', 'img'], recursive=True)
                       if tag.name != 'img' or tag.get('alt'))

    return title_text, content

def crawl_website(start_url, max_duration=120, crawl_delay=1.5):
    visited = set()
    to_visit = deque([start_url])
    base_netloc = urlparse(start_url).netloc
    start_time = time.time()
    results = []

    while to_visit and (time.time() - start_time < max_duration):
        current_url = to_visit.popleft()
        if current_url in visited:
            continue
        visited.add(current_url)

        html = fetch_page(current_url)
        if html is None:
            continue

        title, text = extract_important_text(html)

        if text.strip():
            results.append({"url": current_url, "title": title, "content": text})

        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            absolute_url = urljoin(current_url, link['href'])
            if urlparse(absolute_url).netloc == base_netloc and absolute_url not in visited:
                to_visit.append(absolute_url)

        time.sleep(crawl_delay)

    return results

@app.route('/get-data', methods=['POST'])
def get_data():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' in JSON body"}), 400

    url = data['url']
    results = crawl_website(url)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
