# -*- coding: utf-8 -*-
import sqlite3, json, html

c = sqlite3.connect("corpus_filtered.db")
rows = c.execute("SELECT title, author, date, category, content, url FROM stories").fetchall()

data = [
    {"title": t or "", "author": a or "", "date": d or "",
     "category": cat or "", "content": txt or "", "url": u or ""}
    for (t, a, d, cat, txt, u) in rows
]
payload = json.dumps(data, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Корпус страшных историй — таблица</title>
<style>
  body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 20px; color: #222; }
  h1 { font-size: 22px; margin: 0 0 4px; }
  .sub { color: #666; margin-bottom: 16px; }
  #q { padding: 8px 12px; width: 100%; max-width: 480px; font-size: 15px;
       border: 1px solid #ccc; border-radius: 6px; margin-bottom: 8px; }
  #count { color: #666; font-size: 13px; margin-bottom: 12px; }
  table { border-collapse: collapse; width: 100%; font-size: 14px; }
  th, td { padding: 6px 10px; border-bottom: 1px solid #eee; text-align: left;
           vertical-align: top; }
  th { background: #f5f5f5; cursor: pointer; user-select: none;
       position: sticky; top: 0; z-index: 2; }
  th:hover { background: #e9e9e9; }
  th.asc::after { content: " ▲"; color: #888; font-size: 11px; }
  th.desc::after { content: " ▼"; color: #888; font-size: 11px; }
  tr:hover td { background: #fafafa; }
  td.content { max-width: 620px; }
  td.content .short { display: block; }
  td.content .full { display: none; white-space: pre-wrap; }
  td.content.open .short { display: none; }
  td.content.open .full { display: block; }
  .toggle { color: #0a66c2; cursor: pointer; font-size: 12px; }
  a { color: #0a66c2; text-decoration: none; }
  a:hover { text-decoration: underline; }
</style>
</head>
<body>
<h1>Корпус страшных историй</h1>
<div class="sub">strashilka.com — отфильтрованный корпус (без общих и служебных категорий)</div>
<input id="q" type="search" placeholder="Поиск по заголовку, автору, категории, тексту...">
<div id="count"></div>
<table id="t">
<thead>
<tr>
  <th data-k="title">Заголовок</th>
  <th data-k="author">Автор</th>
  <th data-k="date">Дата</th>
  <th data-k="category">Категория</th>
  <th data-k="content">Текст</th>
  <th data-k="url">Ссылка</th>
</tr>
</thead>
<tbody></tbody>
</table>

<script>
const DATA = __PAYLOAD__;
const tbody = document.querySelector("#t tbody");
const q = document.getElementById("q");
const countEl = document.getElementById("count");
let sortKey = null, sortDir = 1;

function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function render(rows) {
  tbody.innerHTML = "";
  const frag = document.createDocumentFragment();
  for (const r of rows) {
    const tr = document.createElement("tr");
    const shortText = r.content.length > 220 ? r.content.slice(0, 220) + "…" : r.content;
    tr.innerHTML =
      `<td>${esc(r.title)}</td>` +
      `<td>${esc(r.author)}</td>` +
      `<td>${esc(r.date)}</td>` +
      `<td>${esc(r.category)}</td>` +
      `<td class="content"><span class="short">${esc(shortText)}</span>` +
      `<span class="full">${esc(r.content)}</span>` +
      (r.content.length > 220 ? ` <span class="toggle">показать</span>` : "") +
      `</td>` +
      `<td>${r.url ? `<a href="${esc(r.url)}" target="_blank">источник</a>` : ""}</td>`;
    frag.appendChild(tr);
  }
  tbody.appendChild(frag);
  countEl.textContent = `Показано: ${rows.length} из ${DATA.length}`;
}

tbody.addEventListener("click", (e) => {
  if (!e.target.classList.contains("toggle")) return;
  const td = e.target.closest("td.content");
  td.classList.toggle("open");
  e.target.textContent = td.classList.contains("open") ? "свернуть" : "показать";
});

function applyFilter() {
  const needle = q.value.trim().toLowerCase();
  let rows = DATA;
  if (needle) {
    rows = DATA.filter(r =>
      r.title.toLowerCase().includes(needle) ||
      r.author.toLowerCase().includes(needle) ||
      r.category.toLowerCase().includes(needle) ||
      r.date.toLowerCase().includes(needle) ||
      r.content.toLowerCase().includes(needle)
    );
  }
  if (sortKey) {
    rows = rows.slice().sort((a, b) => {
      const A = (a[sortKey] || "").toString().toLowerCase();
      const B = (b[sortKey] || "").toString().toLowerCase();
      return A < B ? -sortDir : A > B ? sortDir : 0;
    });
  }
  render(rows);
}

document.querySelectorAll("#t th").forEach(th => {
  th.addEventListener("click", () => {
    const k = th.dataset.k;
    if (sortKey === k) sortDir *= -1;
    else { sortKey = k; sortDir = 1; }
    document.querySelectorAll("#t th").forEach(x => x.classList.remove("asc", "desc"));
    th.classList.add(sortDir === 1 ? "asc" : "desc");
    applyFilter();
  });
});

q.addEventListener("input", applyFilter);

applyFilter();
</script>
</body>
</html>
"""

out = HTML.replace("__PAYLOAD__", payload)
with open("corpus_table.html", "w", encoding="utf-8") as f:
    f.write(out)
print("saved corpus_table.html")
