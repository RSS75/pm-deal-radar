from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import feedparser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RSS_FEEDS = [
    "https://www.privateequityinternational.com/feed/",
    "https://www.inframationnews.com/feed/",
    "https://www.ft.com/rss/home"
]

def detect_fx(text):
    return "europe" in text.lower() or "usd" in text.lower()

def detect_ir(text):
    return "debt" in text.lower() or "financing" in text.lower()

def detect_region(text):
    if "europe" in text.lower(): return "Europe"
    if "asia" in text.lower(): return "Asia"
    return "Global"

@app.get("/events")
def events():
    out = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for e in feed.entries[:10]:
            text = e.title

            out.append({
                "title": e.title,
                "fx": detect_fx(text),
                "ir": detect_ir(text),
                "region": detect_region(text),
                "size": 1000000000,
                "debt_ratio": 0.6,
                "article_url": e.link,
                "manager_url": "https://www.google.com/search?q=" + e.title.replace(" ","+")
            })
    return out
