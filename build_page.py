#!/usr/bin/env python3
"""Génère le site statique (GitHub Pages) à partir des fichiers data/AAAA-MM-JJ.json.

Usage: python3 build_page.py
Produit: index.html (semaine la plus récente) et archive/AAAA-MM-JJ.html (chaque semaine).
Une semaine = un fichier JSON: {start, end, comment, items: [{p, cat, maxi, iga}]}
où maxi/iga = {price, unit, best, note, regular?}.
"""
import glob
import html
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
MONTHS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]

CSS = """
:root{--bg:#fff;--fg:#1d1d1b;--muted:#6b6b66;--line:#e3e1da;--panel:#f6f5f0;--best:#1a7f4b}
@media(prefers-color-scheme:dark){:root{--bg:#1b1b19;--fg:#f1efe8;--muted:#a3a29a;--line:#333330;--panel:#252523;--best:#5fcf93}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.4 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:560px;margin:0 auto;padding:16px 12px 48px}
h1{font-size:20px;margin:4px 0 4px}
.sub{color:var(--muted);font-size:14px;margin:0 0 14px}
table{width:100%;border-collapse:collapse;font-size:15px}
th,td{text-align:left;padding:8px 6px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:13px;color:var(--muted);font-weight:600}
td.price{white-space:nowrap}
tr.cat td{background:var(--panel);font-size:12px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);padding:6px}
.best{font-weight:700;color:var(--best)}
.none{color:var(--muted)}
sup{color:var(--muted)}
.notes{margin-top:14px;font-size:13px;color:var(--muted)}
.notes p{margin:4px 0}
.legend{margin-top:16px;font-size:13px;color:var(--muted)}
h2{font-size:16px;margin:24px 0 8px}
ul.weeks{padding-left:18px;margin:0}
a{color:inherit}
"""


def fmt_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]}"


def fmt_price(offer):
    if not offer or offer.get("price") is None:
        return None
    s = f"{offer['price']:.2f}".replace(".", ",") + " " + offer.get("unit", "$")
    return s


def render_week(week, weeks_index, is_archive):
    e = html.escape
    rows, notes, n = [], [], 0
    cats = []
    for it in week["items"]:
        c = it.get("cat", "Autres")
        if c not in cats:
            cats.append(c)
    for c in cats:
        rows.append(f'<tr class="cat"><td colspan="3">{e(c)}</td></tr>')
        for it in [x for x in week["items"] if x.get("cat", "Autres") == c]:
            cells = [f"<td>{e(it['p'])}</td>"]
            for store in ("maxi", "iga"):
                offer = it.get(store)
                price = fmt_price(offer)
                if price is None:
                    cells.append('<td class="price none">—</td>')
                    continue
                if offer.get("regular") is not None:
                    price += f" ({offer['regular']:.2f}".replace(".", ",") + " $)"
                cls = "price best" if offer.get("best") else "price"
                mark = ""
                if offer.get("note"):
                    n += 1
                    mark = f"<sup> {n}</sup>"
                    notes.append(f"{n}. {it['p']} ({store.capitalize() if store == 'maxi' else 'IGA'}): {offer['note']}")
                cells.append(f'<td class="{cls}">{e(price)}{mark}</td>')
            rows.append("<tr>" + "".join(cells) + "</tr>")
    notes_html = "".join(f"<p>{e(t)}</p>" for t in notes)
    prefix = "../" if is_archive else ""
    weeks_html = "".join(
        f'<li><a href="{prefix}archive/{w["start"]}.html">Semaine du {fmt_date(w["start"])} au {fmt_date(w["end"])}</a></li>'
        for w in weeks_index
    )
    back = f'<p class="sub"><a href="{prefix}index.html">← Semaine la plus récente</a></p>' if is_archive else ""
    comment = f'<p class="legend">{e(week.get("comment", ""))}</p>' if week.get("comment") else ""
    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rabais d'épicerie – Maxi vs IGA</title><style>{CSS}</style></head>
<body><main>
<h1>Rabais d'épicerie – Maxi vs IGA</h1>
<p class="sub">Circulaires du {fmt_date(week['start'])} au {fmt_date(week['end'])} · région de Québec</p>
{back}
<table><thead><tr><th>Produit</th><th>Maxi</th><th>IGA</th></tr></thead><tbody>
{''.join(rows)}
</tbody></table>
<div class="notes">{notes_html}</div>
<p class="legend">En gras vert: le meilleur prix entre les deux épiceries. Prix tirés des circulaires et des sites des épiceries, à valider en magasin: ils peuvent varier selon la succursale. Projet personnel, non affilié à Maxi ni à IGA.</p>
{comment}
<h2>Autres semaines</h2><ul class="weeks">{weeks_html}</ul>
</main></body></html>
"""


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "data", "*.json")))
    weeks = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            weeks.append(json.load(fh))
    weeks.sort(key=lambda w: w["start"], reverse=True)
    if not weeks:
        raise SystemExit("Aucune donnée dans data/")
    os.makedirs(os.path.join(ROOT, "archive"), exist_ok=True)
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(render_week(weeks[0], weeks, False))
    for w in weeks:
        with open(os.path.join(ROOT, "archive", f"{w['start']}.html"), "w", encoding="utf-8") as fh:
            fh.write(render_week(w, weeks, True))
    open(os.path.join(ROOT, ".nojekyll"), "w").close()
    print(f"OK: {len(weeks)} semaine(s), plus récente: {weeks[0]['start']}")


if __name__ == "__main__":
    main()
