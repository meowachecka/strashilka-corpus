# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

c = sqlite3.connect("corpus_filtered.db")
df = pd.read_sql_query("SELECT category, date, content FROM stories", c)
df["year"] = df["date"].str[-4:]
df = df[~df["year"].isin(["007", "666"])]
df["length"] = df["content"].str.len()

# 1. Категории
fig, ax = plt.subplots(figsize=(9, 6))
df["category"].value_counts().plot(kind="barh", ax=ax, color="steelblue")
ax.set_title("Отфильтрованный корпус: распределение по категориям")
ax.set_xlabel("число историй")
ax.invert_yaxis()
plt.tight_layout(); plt.savefig("plot_categories.png", dpi=120); plt.close()

# 2. По годам
fig, ax = plt.subplots(figsize=(10, 5))
by_year = df["year"].value_counts().sort_index()
by_year = by_year[by_year.index.str.isdigit()]
by_year.plot(kind="bar", ax=ax, color="darkorange")
ax.set_title("Динамика публикаций по годам")
ax.set_xlabel("год"); ax.set_ylabel("число историй")
plt.tight_layout(); plt.savefig("plot_years.png", dpi=120); plt.close()

# 3. Распределение длины
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df["length"], bins=60, color="seagreen")
ax.set_title("Распределение длины текстов")
ax.set_xlabel("символы"); ax.set_ylabel("число историй")
plt.tight_layout(); plt.savefig("plot_lengths.png", dpi=120); plt.close()

print("saved: plot_categories.png, plot_years.png, plot_lengths.png")
