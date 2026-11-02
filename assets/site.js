'use strict';

// Reuse the first three entries from the full journal list, including forthcoming papers.
const recentJournals = document.querySelector('[data-recent-journals]');
if (recentJournals) {
  async function loadRecentJournals() {
    try {
      const response = await fetch('publications.html', { cache: 'no-cache' });
      if (!response.ok) throw new Error(`Publication list returned ${response.status}`);
      const publicationPage = new DOMParser().parseFromString(await response.text(), 'text/html');
      const journalGroup = publicationPage.querySelector('[data-group="journal"]');
      if (!journalGroup) throw new Error('Journal section is missing');
      const papers = [...journalGroup.querySelectorAll('.publication')].slice(0, 3);
      const copies = papers.map(paper => {
        const copy = document.importNode(paper, true);
        copy.id = `home-${paper.id}`;
        return copy;
      });
      recentJournals.replaceChildren(...copies);
      recentJournals.dataset.loaded = 'true';
    } catch (error) {
      // Keep the readable HTML fallback when the network or JavaScript is unavailable.
      console.warn('Could not refresh recent journals; keeping the saved list.', error);
    }
  }
  loadRecentJournals();
}

const controls = document.querySelector('.publication-controls');
if (controls) {
  const search = document.querySelector('#publication-search');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const papers = [...document.querySelectorAll('.all-publications .publication')];
  const groups = [...document.querySelectorAll('[data-group]')];
  const count = document.querySelector('.result-count');
  const empty = document.querySelector('.empty-state');
  let category = 'all';
  const searchable = new Map(papers.map(paper => [paper, paper.textContent.toLocaleLowerCase().normalize('NFKC')]));

  function filterPublications() {
    const terms = search.value.toLocaleLowerCase().normalize('NFKC').trim().split(/\s+/).filter(Boolean);
    let visible = 0;
    papers.forEach(paper => {
      const matches = (category === 'all' || paper.dataset.category === category)
        && terms.every(term => searchable.get(paper).includes(term));
      paper.hidden = !matches;
      if (matches) visible++;
    });
    groups.forEach(group => {
      const visiblePapers = [...group.querySelectorAll('.publication')].filter(paper => !paper.hidden);
      group.hidden = visiblePapers.length === 0;
      group.querySelector('h2 span').textContent = String(visiblePapers.length).padStart(2, '0');
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
    count.textContent = `Showing ${visible} of ${papers.length} publication${papers.length === 1 ? '' : 's'}`;
    empty.hidden = visible > 0;
  }

  search.addEventListener('input', filterPublications);
  buttons.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    filterPublications();
  }));
  document.querySelector('#reset-search').addEventListener('click', () => {
    category = 'all';
    search.value = '';
    filterPublications();
    search.focus();
  });
  controls.hidden = false;
  filterPublications();
}
