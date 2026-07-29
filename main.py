from fastapi import FastAPI
from crawler.sources import SOURCES
from crawler.html_crawler import scrape_html_source

app = FastAPI()
jobs_db = []

@app.get("/")
async def home():
    return {"message": "Govt Vacancy Scanner is running!", "status": "active"}

@app.get("/scrape")
async def scrape_all():
    global jobs_db
    all_jobs = []
    for source in SOURCES:
        try:
            jobs = scrape_html_source(source)
            all_jobs.extend(jobs)
        except Exception as e:
            print(f"Error: {e}")
    jobs_db = all_jobs
    return {"status": "ok", "count": len(jobs_db), "jobs": jobs_db}
