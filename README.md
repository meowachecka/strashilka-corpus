# strashilka-corpus

Корпус страшных историй с https://strashilka.com/

## Состав
- `scraper.py` — парсер (curl_cffi + BeautifulSoup, пауза 2–5 с, robots.txt соблюдён)
- `corpus.db` — SQLite, таблица `stories`: title, author, date, category, content, url, text_hash
- Дедупликация — по md5(content): UNIQUE + INSERT OR IGNORE

## Запуск
python3 -m venv .venv && source .venv/bin/activate
pip install curl_cffi beautifulsoup4
python scraper.py

## Данные
Собрано с соблюдением robots.txt (Crawl-delay: 1), пауза 2–5 с между запросами.
Материалы принадлежат авторам; корпус собран в исследовательских целях.
