import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.text

def parse_jobs_from_html(html, source):
    soup = BeautifulSoup(html, "lxml")
    job_items = soup.select(source["job_list_selector"])
    jobs = []
    for item in job_items:
        title_elem = item.select_one(source["title_selector"])
        link_elem = item.select_one(source["link_selector"])
        date_elem = item.select_one(source["date_selector"]) if "date_selector" in source else None

        title = title_elem.text.strip() if title_elem else "N/A"
        link = link_elem.get("href") if link_elem else ""
        if link and not link.startswith("http"):
            link = source["url"].rstrip("/") + "/" + link.lstrip("/")
        date = date_elem.text.strip() if date_elem else "N/A"

        jobs.append({
            "source": source["name"],
            "title": title,
            "link": link,
            "date": date,
        })
    return jobs

def scrape_html_source(source):
    html = fetch_html(source["url"])
    return parse_jobs_from_html(html, source)
