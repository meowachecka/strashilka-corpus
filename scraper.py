# -*- coding: utf-8 -*-
import time, random, sqlite3, hashlib, re
from curl_cffi import requests
from bs4 import BeautifulSoup

BASE = "https://strashilka.com"
MAX_PAGES = 2200
DB = "corpus.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_hash TEXT UNIQUE,
    title TEXT,
    author TEXT,
    date TEXT,
    category TEXT,
    content TEXT,
    url TEXT
)
""")
conn.commit()

HEADERS = {"Accept-Language": "ru-RU,ru;q=0.9"}

def get(url):
    r = requests.get(url, impersonate="chrome124", headers=HEADERS, timeout=30)
    if r.status_code != 200:
        print(f"  ! status {r.status_code} na {url}")
        return None
    return r.text

def parse_entry(entry):
    a = entry.select_one(".entry-header h3 a")
    if not a:
        return None
    title = a.get_text(strip=True)
    url = a["href"]

    author_tag = entry.select_one(".entry-author a")
    author = author_tag.get_text(strip=True) if author_tag else ""

    author_text = entry.select_one(".entry-author").get_text(" ", strip=True)
    m = re.search(r"от\s*([\d\-]+\s*[\d:]+)", author_text)
    date = m.group(1) if m else ""

    cat_tag = entry.select_one(".entry-cat a")
    category = cat_tag.get_text(strip=True) if cat_tag else ""

    text_div = entry.select_one(".entry-text > div")
    if not text_div:
        return None
    for br in text_div.find_all("br"):
        br.replace_with("\n")
    content = text_div.get_text()
    content = re.sub(r"[ \t]+", " ", content)
    content = re.sub(r"\n{3,}", "\n\n", content).strip()

    if len(content) < 50:
        return None

    return {
        "title": title, "author": author, "date": date,
        "category": category, "content": content, "url": url,
        "text_hash": hashlib.md5(content.encode("utf-8")).hexdigest(),
    }

def scrape():
    total_new = 0
    for page in range(1, MAX_PAGES + 1):
        url = f"{BASE}/" if page == 1 else f"{BASE}/page/{page}/"
        print(f"[{page}] {url}")
        html = get(url)
        if not html:
            break
        soup = BeautifulSoup(html, "html.parser")
        entries = soup.select("div.entry")
        if not entries:
            print("  net istoriy - stop")
            break
        for e in entries:
            d = parse_entry(e)
            if not d:
                continue
            cur.execute("""INSERT OR IGNORE INTO stories
                (text_hash,title,author,date,category,content,url)
                VALUES (?,?,?,?,?,?,?)""",
                (d["text_hash"], d["title"], d["author"], d["date"],
                 d["category"], d["content"], d["url"]))
            if cur.rowcount:
                total_new += 1
        conn.commit()
        n = cur.execute('SELECT COUNT(*) FROM stories').fetchone()[0]
        print(f"  vsego v baze: {n}")
        pause = random.uniform(2, 5)
        print(f"  pauza {pause:.1f} s")
        time.sleep(pause)

    print(f"\nGotovo. Novyh istoriy: {total_new}")
    conn.close()

if __name__ == "__main__":
    scrape()
