# -*- coding: utf-8 -*-
import sqlite3, csv

c = sqlite3.connect("corpus.db")
with open("corpus.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["title", "author", "date", "category", "content", "url", "text_hash"])
    for row in c.execute("SELECT title,author,date,category,content,url,text_hash FROM stories"):
        w.writerow(row)
print("saved corpus.csv")
