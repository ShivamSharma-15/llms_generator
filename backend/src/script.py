import sys
import json
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

def extract_content(soup):
    title = soup.title.string.strip() if soup.title else "No Title"
    paragraphs = soup.find_all('p')
    text = " ".join(p.get_text().strip() for p in paragraphs)
    return title, text

def is_valid_url(url, base_netloc):
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and parsed.netloc == base_netloc

def crawl_website(start_url, max_duration=120):
    visited = set()
    to_visit = deque([start_url])
    base_netloc = urlparse(start_url).netloc
    start_time = time.time()
    results = []

    while to_visit and time.time() - start_time < max_duration:
        current_url = to_visit.popleft()
        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            res = requests.get(current_url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')

            title, text = extract_content(soup)
            if text.strip():  # Avoid empty pages
                results.append({
                    "url": current_url,
                    "title": title,
                    "content": text[:2000] + "..." if len(text) > 2000 else text
                })

            # Discover internal links
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(current_url, link['href'])
                if is_valid_url(absolute_url, base_netloc) and absolute_url not in visited:
                    to_visit.append(absolute_url)

        except Exception as e:
            results.append({"url": current_url, "error": str(e)})

    return results

def main():
    if len(sys.argv) > 1:
        data = json.loads(sys.argv[1])
        url = data.get("url")
        if not url:
            print(json.dumps({"error": "URL is missing"}))
            return
        results = crawl_website(url)
        print(json.dumps(results, indent=2))
    else:
        print(json.dumps({"error": "No input provided"}))

if __name__ == "__main__":
    main()
