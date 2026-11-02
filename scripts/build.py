#!/usr/bin/env python3
"""Regenerate the static pages. Uses only the Python standard library."""
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
    kind = 'Journal' if p['category'] == 'journal' else 'Conference'
    if p['category'].startswith('korean-'):
        kind = 'Korean ' + ('journal' if p['category'] == 'korean-journal' else 'conference')
    public_pdf = any(l['label'] == 'Open Access PDF' for l in p['links'])
    visible_links = [l for l in p['links'] if not (public_pdf and l['label'] == 'PDF')]
    links = ''.join(f'<a href="{escape(l["url"], quote=True)}">{escape("PDF (lab access)" if l["label"] == "PDF" and "/publications/original/" in l["url"] else l["label"])} <span aria-hidden="true">↗</span></a>' for l in visible_links)
    award = '<span class="award">Best Paper Award</span>' if p['award'] else ''
    ident = ('selected-' if compact else '') + p['id']
    lang = ' lang="ko"' if p['category'].startswith('korean-') else ''
    return f'''<article class="publication" id="{ident}" data-category="{p['category']}">
        <div class="pub-meta"><span>{kind}</span><span>{p['year']}</span>{award}</div>
        <h3{lang}>{escape(p['title'])}</h3>
        <p class="authors"{lang}>{escape(p['authors'])}</p>
        <p class="venue"{lang}>{escape(p['venue'])}</p>
        <div class="paper-links">{links}</div>
    </article>'''

def page(content, publications=False):
    title = 'Publications | Jaemin Kim' if publications else 'Jaemin Kim | Wireless Networks & Online Learning'
    description = ('Publications by Jaemin Kim in wireless networks, O-RAN, online learning, and federated learning.' if publications else 'Jaemin Kim is a Ph.D. student at Chung-Ang University researching wireless networks, O-RAN, online learning, and resource allocation.')
    canonical = 'https://jmkim-jay.github.io/' + ('publications.html' if publications else '')
    home = 'index.html' if publications else ''
    current_about = '' if publications else ' aria-current="page"'
    current_pubs = ' aria-current="page"' if publications else ''
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f8f9f6">
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
    <div class="header-inner">
      <a class="brand" href="index.html" aria-label="Jaemin Kim — home"><span class="monogram" aria-hidden="true">jk.</span><span>Jaemin Kim</span></a>
      <nav aria-label="Main navigation">
        <a href="{home}#about"{current_about}>About</a>
        <a href="{home}#research">Research</a>
        <a href="publications.html"{current_pubs}>Publications</a>
        <a href="{home}#experience">Experience</a>
      </nav>
    </div>
  </header>
  <div class="page-layout">
    <aside class="profile" aria-label="Profile and contact">
      <div class="portrait-frame"><img src="assets/portrait.jpeg" alt="Portrait of Jaemin Kim" width="120" height="154" fetchpriority="high"></div>
      <p class="profile-name">Jaemin Kim <span lang="ko">김재민</span></p>
      <p class="profile-role">Ph.D. Student</p>
      <p class="profile-affiliation">Computer Science &amp; Engineering<br>Chung-Ang University</p>
      <div class="profile-divider"></div>
      <a class="profile-link" href="mailto:jmkim@uclab.re.kr"><span class="link-label">Email</span><span>jmkim@uclab.re.kr ↗</span></a>
      <a class="profile-link" href="https://github.com/jmkim-jay"><span class="link-label">Code</span><span>GitHub ↗</span></a>
      <a class="profile-link" href="https://uclab.re.kr/jmkim.html"><span class="link-label">Lab</span><span>UCLab ↗</span></a>
      <p class="profile-note">Wireless networks.<br>Online learning.<br>Real-time decisions.</p>
    </aside>
    <main id="main">{content}</main>
  </div>
  <footer class="site-footer"><span>© 2026 Jaemin Kim</span><a href="#main">Back to top ↑</a></footer>
</body>
</html>
'''

selected_ids = ['journal-2', 'conference-15', 'journal-3', 'journal-1', 'conference-11', 'conference-14']
by_id = {p['id']: p for p in PUBLICATIONS}
selected = '\n'.join(publication(by_id[i], compact=True) for i in selected_ids)
home = f'''
<section class="intro" id="about" aria-labelledby="intro-title">
  <p class="eyebrow"><span class="small-rule"></span> Wireless networks &amp; intelligent control</p>
  <h1 id="intro-title">Jaemin Kim<span class="name-dot">.</span></h1>
  <p class="intro-subtitle">Researching how wireless networks learn, adapt, and allocate resources.</p>
  <div class="intro-copy">
    <p>I am a Ph.D. student in Computer Science and Engineering at <a href="https://www.cau.ac.kr/">Chung-Ang University</a>, advised by Prof. Sungrae Cho at <a href="https://uclab.re.kr/">UCLab</a>.</p>
    <p>My research focuses on <strong>real-time control and resource allocation in O-RAN</strong>, with an emphasis on online learning and optimization. I am also interested in federated learning over wireless networks and digital twin-assisted network control.</p>
    <p>In November–December 2026, I am visiting <a href="https://www.northeastern.edu/">Northeastern University</a> to collaborate with Prof. Tommaso Melodia and WiNEs Lab.</p>
  </div>
  <div class="intro-actions"><a class="button" href="publications.html">Explore publications <span aria-hidden="true">↗</span></a><a class="text-link" href="mailto:jmkim@uclab.re.kr">Get in touch <span aria-hidden="true">↗</span></a></div>
</section>

<section class="section" id="research" aria-labelledby="research-title">
  <div class="section-heading"><p class="section-number">01</p><h2 id="research-title">Research interests</h2></div>
  <div class="research-list">
    <article><span class="research-index">I</span><div><h3>O-RAN &amp; real-time control</h3><p>Radio resource allocation, scheduling, and closed-loop control for adaptive wireless networks.</p></div><span class="research-tag">NETWORKS</span></article>
    <article><span class="research-index">II</span><div><h3>Online learning &amp; optimization</h3><p>Sequential decision-making and online convex optimization under changing network conditions.</p></div><span class="research-tag">METHODS</span></article>
    <article><span class="research-index">III</span><div><h3>Wireless federated learning</h3><p>Energy-efficient device scheduling, communication, and learning with dynamic data.</p></div><span class="research-tag">LEARNING</span></article>
  </div>
</section>

<section class="section" id="news" aria-labelledby="news-title">
  <div class="section-heading"><p class="section-number">02</p><h2 id="news-title">Recently</h2></div>
  <div class="news-list">
    <article><time datetime="2026-11">Nov 2026</time><p>Visiting WiNEs Lab at Northeastern University for a two-month research stay.</p></article>
    <article><time datetime="2026-08">Aug 2026</time><p><a href="https://ieeexplore.ieee.org/document/11421057">Energy-Efficient Online Federated Learning in Wireless Networks</a> appears in <em>IEEE Transactions on Vehicular Technology</em>.</p></article>
  </div>
</section>

<section class="section" id="selected-publications" aria-labelledby="selected-title">
  <div class="section-heading"><p class="section-number">03</p><h2 id="selected-title">Selected publications</h2><a class="section-link" href="publications.html">View all ↗</a></div>
  <div class="publication-list">{selected}</div>
</section>

<section class="section" id="experience" aria-labelledby="experience-title">
  <div class="section-heading"><p class="section-number">04</p><h2 id="experience-title">Education &amp; experience</h2></div>
  <div class="timeline">
    <article><p class="timeline-date">Nov–Dec 2026</p><div><h3>Visiting Researcher</h3><p>Northeastern University · WiNEs Lab</p><p class="muted">Host: Prof. Tommaso Melodia</p></div></article>
    <article><p class="timeline-date">Current</p><div><h3>Ph.D. in Computer Science &amp; Engineering</h3><p>Chung-Ang University</p><p class="muted">Advisor: Prof. Sungrae Cho</p></div></article>
    <article><p class="timeline-date">2025</p><div><h3>M.S. in Computer Science &amp; Engineering</h3><p>Chung-Ang University</p></div></article>
    <article><p class="timeline-date">2023</p><div><h3>B.S. in Computer Science &amp; Engineering</h3><p>Chung-Ang University</p></div></article>
  </div>
</section>

<section class="contact-section" id="contact" aria-labelledby="contact-title">
  <p class="eyebrow">LET’S CONNECT</p><h2 id="contact-title">Ideas are better shared.</h2>
  <p>For research discussions and collaboration in wireless networks, online learning, and O-RAN:</p>
  <a class="contact-email" href="mailto:jmkim@uclab.re.kr">jmkim@uclab.re.kr <span aria-hidden="true">↗</span></a>
</section>'''

groups = ''
filters = f'<button type="button" data-filter="all" aria-pressed="true">All <span>{len(PUBLICATIONS)}</span></button>'
for key, label in CATEGORIES:
    records = [p for p in PUBLICATIONS if p['category'] == key]
    filters += f'<button type="button" data-filter="{key}" aria-pressed="false">{label} <span>{len(records)}</span></button>'
    groups += f'<section class="pub-group" data-group="{key}" aria-labelledby="heading-{key}"><h2 id="heading-{key}">{label} <span>{len(records):02}</span></h2>' + ''.join(publication(p) for p in records) + '</section>'

pubs = f'''
<section class="intro publications-intro"><p class="eyebrow"><span class="small-rule"></span> Publications</p><h1>Research record<span class="name-dot">.</span></h1><p class="intro-subtitle">Work on wireless networks, learning, and resource allocation.</p><p class="record-source">Publication details and paper links from my <a href="https://uclab.re.kr/jmkim.html">UCLab profile ↗</a>. Links marked “lab access” may require UCLab credentials.</p></section>
<div class="publication-controls" hidden>
  <label class="search-label" for="publication-search">Search publications</label>
  <input id="publication-search" type="search" placeholder="Search by title, author, topic, or year…" autocomplete="off">
  <div class="filter-buttons" role="group" aria-label="Publication category">{filters}</div>
  <p class="result-count" role="status" aria-live="polite" aria-atomic="true">Showing {len(PUBLICATIONS)} publications</p>
</div>
<div class="all-publications">{groups}</div>
<div class="empty-state" hidden><h2>No matching publications</h2><p>Try a different keyword or choose another category.</p><button type="button" class="button" id="reset-search">Clear filters</button></div>
'''

(ROOT / 'index.html').write_text(page(home), encoding='utf-8')
(ROOT / 'publications.html').write_text(page(pubs, publications=True), encoding='utf-8')
print(f'Generated index.html and publications.html ({len(PUBLICATIONS)} publications).')
