#!/usr/bin/env python3
"""Generate a minimal, accessible academic website without dependencies."""
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


def publication(p, compact=False):
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
    ident = ('selected-' if compact else '') + p['id']
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


def page(content, publications=False):
    title = 'Publications — Jaemin Kim' if publications else 'Jaemin Kim'
    description = ('Publications by Jaemin Kim in wireless networks, O-RAN, online learning, and federated learning.' if publications else 'Jaemin Kim is a Ph.D. student at Chung-Ang University researching wireless networks, O-RAN, online learning, and resource allocation.')
    canonical = 'https://jmkim-jay.github.io/' + ('publications.html' if publications else '')
    home = 'index.html' if publications else ''
    about_current = '' if publications else ' aria-current="page"'
    pubs_current = ' aria-current="page"' if publications else ''
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
      <a href="{home}#about"{about_current}>About</a>
      <a href="publications.html"{pubs_current}>Publications</a>
      <a href="{home}#experience">Experience</a>
    </nav>
  </header>
  <main id="main">{content}</main>
  <footer class="site-footer">
    <span>© 2026 Jaemin Kim</span>
    <div><a href="mailto:jmkim@uclab.re.kr">Email</a><a href="https://github.com/jmkim-jay">GitHub ↗</a><a href="#main">Top ↑</a></div>
  </footer>
</body>
</html>
'''


selected_ids = ['journal-2', 'conference-15', 'journal-3', 'journal-1']
by_id = {p['id']: p for p in PUBLICATIONS}
selected = '\n'.join(publication(by_id[i], compact=True) for i in selected_ids)
home = f'''
<section class="intro" id="about" aria-labelledby="intro-title">
  <div class="intro-header">
    <div><h1 id="intro-title">Jaemin Kim <span lang="ko">김재민</span></h1>
      <p class="role">Ph.D. student · Chung-Ang University</p>
      <p class="field">Wireless networks, online learning &amp; optimization</p>
    </div>
    <img class="portrait" src="assets/portrait.jpeg" alt="Portrait of Jaemin Kim" width="120" height="154" fetchpriority="high">
  </div>
  <div class="bio">
    <p>I am a Ph.D. student in Computer Science and Engineering at <a href="https://www.cau.ac.kr/">Chung-Ang University</a>, advised by Prof. Sungrae Cho at <a href="https://uclab.re.kr/">UCLab</a>. I study real-time control and resource allocation in wireless networks, especially O-RAN.</p>
    <p>In November–December 2026, I am a visiting researcher at <a href="https://www.northeastern.edu/">Northeastern University</a>, collaborating with Prof. Tommaso Melodia and WiNEs Lab.</p>
  </div>
  <div class="contact-links" aria-label="Contact and profiles">
    <a href="mailto:jmkim@uclab.re.kr">jmkim@uclab.re.kr <span aria-hidden="true">↗</span></a>
    <a href="https://github.com/jmkim-jay">GitHub <span aria-hidden="true">↗</span></a>
    <a href="https://uclab.re.kr/jmkim.html">UCLab profile <span aria-hidden="true">↗</span></a>
  </div>
</section>

<section class="section" id="research" aria-labelledby="research-title">
  <div class="section-heading"><h2 id="research-title">Research</h2></div>
  <div class="research-grid">
    <article><h3>O-RAN control</h3><p>Radio resource allocation, scheduling, and real-time decision-making.</p></article>
    <article><h3>Online learning</h3><p>Sequential optimization under changing network conditions.</p></article>
    <article><h3>Wireless federated learning</h3><p>Energy-efficient device scheduling and communication.</p></article>
    <article><h3>Network digital twins</h3><p>Digital twin-assisted control and synchronization.</p></article>
  </div>
</section>

<section class="section" id="news" aria-labelledby="news-title">
  <div class="section-heading"><h2 id="news-title">News</h2></div>
  <div class="news-list">
    <article><time datetime="2026-11">Nov 2026</time><p>Joining WiNEs Lab at Northeastern University as a visiting researcher.</p></article>
    <article><time datetime="2026-08">Aug 2026</time><p>Our work on <a href="https://ieeexplore.ieee.org/document/11421057">energy-efficient online federated learning</a> appears in <em>IEEE TVT</em>.</p></article>
  </div>
</section>

<section class="section" id="selected-publications" aria-labelledby="selected-title">
  <div class="section-heading"><h2 id="selected-title">Selected publications</h2><a class="section-link" href="publications.html">All publications <span aria-hidden="true">↗</span></a></div>
  <div class="publication-list">{selected}</div>
</section>

<section class="section" id="experience" aria-labelledby="experience-title">
  <div class="section-heading"><h2 id="experience-title">Education &amp; experience</h2></div>
  <div class="timeline">
    <article><p class="timeline-date">Nov–Dec 2026</p><div><h3>Visiting Researcher</h3><p>Northeastern University · WiNEs Lab</p><p class="detail">Host: Prof. Tommaso Melodia</p></div></article>
    <article><p class="timeline-date">Current</p><div><h3>Ph.D. student, Computer Science &amp; Engineering</h3><p>Chung-Ang University</p><p class="detail">Advisor: Prof. Sungrae Cho</p></div></article>
    <article><p class="timeline-date">2025</p><div><h3>M.S., Computer Science &amp; Engineering</h3><p>Chung-Ang University</p></div></article>
    <article><p class="timeline-date">2023</p><div><h3>B.S., Computer Science &amp; Engineering</h3><p>Chung-Ang University</p></div></article>
  </div>
</section>

<section class="contact" id="contact" aria-labelledby="contact-title">
  <h2 id="contact-title">Contact</h2><p>For research discussions and collaboration, reach me at <a href="mailto:jmkim@uclab.re.kr">jmkim@uclab.re.kr</a>.</p>
</section>'''

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


write_page('index.html', page(home))
write_page('publications.html', page(pubs, publications=True))
print(f'Generated 2 pages: {len(selected_ids)} selected / {len(PUBLICATIONS)} total publications.')
