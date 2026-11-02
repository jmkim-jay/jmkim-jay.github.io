#!/usr/bin/env python3
"""Regenerate publications.html only; edit the home page directly in index.html."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLICATIONS = json.loads((ROOT / 'data/publications.json').read_text(encoding='utf-8'))
CATEGORIES = [
    ('journal', 'International journals'),
    ('conference', 'International conferences'),
    ('korean-journal', 'Korean journals'),
    ('korean-conference', 'Korean conferences'),
]


def publication(p):
    public_pdf = any(link['label'] == 'Open Access PDF' for link in p['links'])
    visible_links = [link for link in p['links'] if not (public_pdf and link['label'] == 'PDF')]
    links = []
    for link in visible_links:
        label = link['label']
        if label == 'PDF' and '/publications/original/' in link['url']:
            label = 'PDF (lab access)'
        elif label == 'Open Access PDF':
            label = 'Open PDF'
        links.append(f'<a href="{escape(link["url"], quote=True)}">{escape(label)}<span aria-hidden="true"> ↗</span></a>')
    award = '<span class="award">Best Paper Award</span>' if p['award'] else ''
    ident = p['id']
    lang = ' lang="ko"' if p['category'].startswith('korean-') else ''
    return f'''<article class="publication" id="{ident}" data-category="{p['category']}">
      <p class="pub-year">{p['year']}</p>
      <div class="pub-body">
        <h3{lang}>{escape(p['title'])}</h3>
        <p class="authors"{lang}>{escape(p['authors'])}</p>
        <p class="venue"{lang}>{escape(p['venue'])}</p>
        {award}
        <div class="paper-links">{''.join(links)}</div>
      </div>
    </article>'''


def page(content):
    title = 'Publications — Jaemin Kim'
    description = 'Publications by Jaemin Kim in wireless networks, O-RAN, online learning, and federated learning.'
    canonical = 'https://jmkim-jay.github.io/publications.html'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#ffffff">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/style.css">
  <script src="assets/site.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <a class="brand" href="index.html" aria-label="Jaemin Kim — home">Jaemin Kim</a>
    <nav aria-label="Main navigation">
      <a href="index.html#about">About</a>
      <a href="publications.html" aria-current="page">Publications</a>
      <a href="index.html#experience">Experience</a>
    </nav>
  </header>
  <main id="main">{content}</main>
  <footer class="site-footer">
    <span>© 2026 Jaemin Kim</span>
    <div><a href="mailto:jmkim@uclab.re.kr">Email</a><a href="https://github.com/jmkim-jay">GitHub ↗</a><a href="https://www.linkedin.com/in/jaemin-kim-77413a429/">LinkedIn ↗</a><a href="#main">Top ↑</a></div>
  </footer>
</body>
</html>
'''


groups = ''
filters = f'<button type="button" data-filter="all" aria-pressed="true">All <span>{len(PUBLICATIONS)}</span></button>'
for key, label in CATEGORIES:
    records = [p for p in PUBLICATIONS if p['category'] == key]
    filters += f'<button type="button" data-filter="{key}" aria-pressed="false">{label} <span>{len(records)}</span></button>'
    groups += f'<section class="pub-group" data-group="{key}" aria-labelledby="heading-{key}"><h2 id="heading-{key}">{label} <span>{len(records)}</span></h2>' + ''.join(publication(p) for p in records) + '</section>'

pubs = f'''
<section class="publications-intro"><h1>Publications</h1><p>Research on wireless networks, learning, and resource allocation.</p></section>
<div class="publication-controls" hidden>
  <label class="search-label" for="publication-search">Search publications</label>
  <input id="publication-search" type="search" placeholder="Title, author, topic, or year" autocomplete="off">
  <div class="filter-buttons" role="group" aria-label="Publication category">{filters}</div>
  <p class="result-count" role="status" aria-live="polite" aria-atomic="true">Showing {len(PUBLICATIONS)} publications</p>
</div>
<div class="all-publications">{groups}</div>
<div class="empty-state" hidden><h2>No matching publications</h2><p>Try another keyword or category.</p><button type="button" id="reset-search">Clear filters</button></div>
<p class="record-source">Publication record: <a href="https://uclab.re.kr/jmkim.html">UCLab profile ↗</a>. PDFs marked “lab access” may require UCLab credentials.</p>
'''

def write_page(filename, content):
    cleaned = '\n'.join(line.rstrip() for line in content.splitlines()) + '\n'
    (ROOT / filename).write_text(cleaned, encoding='utf-8')


write_page('publications.html', page(pubs))
print(f'Generated publications.html: {len(PUBLICATIONS)} publications. index.html was not changed.')
