# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

c = sqlite3.connect("corpus.db")
df = pd.read_sql_query("SELECT category, author, date, content FROM stories", c)
df["length"] = df["content"].str.len()

# 1. Категории
fig, ax = plt.subplots(1, 2, figsize=(14, 5))
df["category"].value_counts().head(15).plot(kind="barh", ax=ax[0])
ax[0].set_title("Топ-15 категорий")
ax[0].invert_yaxis()

# 2. Распределение длины
ax[1].hist(df["length"], bins=60)
ax[1].set_title("Распределение длины текстов (символы)")
ax[1].set_xlabel("символы")

plt.tight_layout()
plt.savefig("corpus_stats.png", dpi=120)
print("saved corpus_stats.png")
