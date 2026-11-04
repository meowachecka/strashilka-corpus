# -*- coding: utf-8 -*-
import sqlite3

c = sqlite3.connect("corpus.db")

print("=== ОБЩЕЕ ===")
total = c.execute("SELECT COUNT(*) FROM stories").fetchone()[0]
print("Всего историй:", total)
print("Уникальных авторов:", c.execute("SELECT COUNT(DISTINCT author) FROM stories").fetchone()[0])
print("Категорий:", c.execute("SELECT COUNT(DISTINCT category) FROM stories").fetchone()[0])

print("\n=== ДЛИНА ТЕКСТОВ (символы) ===")
for label, q in [
    ("мин", "MIN(LENGTH(content))"),
    ("средняя", "AVG(LENGTH(content))"),
    ("медиана", None),  # посчитаем отдельно
    ("макс", "MAX(LENGTH(content))"),
]:
    if q:
        v = c.execute(f"SELECT {q} FROM stories").fetchone()[0]
        print(f"  {label}: {v:.0f}" if isinstance(v, float) else f"  {label}: {v}")

lengths = [r[0] for r in c.execute("SELECT LENGTH(content) FROM stories")]
lengths.sort()
print("  медиана:", lengths[len(lengths)//2])

print("\n=== ПО КАТЕГОРИЯМ ===")
for cat, n in c.execute("SELECT category, COUNT(*) FROM stories GROUP BY category ORDER BY 2 DESC"):
    print(f"  {cat or '(без категории)'}: {n}")

print("\n=== ТОП-15 АВТОРОВ ===")
for a, n in c.execute("SELECT author, COUNT(*) FROM stories GROUP BY author ORDER BY 2 DESC LIMIT 15"):
    print(f"  {a}: {n}")

print("\n=== ПО ГОДАМ ===")
# date хранится как '2-11-2026' -> берём последние 4 символа как год
for y, n in c.execute("""
    SELECT SUBSTR(date, -4) AS year, COUNT(*)
    FROM stories
    WHERE date != ''
    GROUP BY year ORDER BY year
"""):
    print(f"  {y}: {n}")
