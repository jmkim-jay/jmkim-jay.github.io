'use strict';

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
