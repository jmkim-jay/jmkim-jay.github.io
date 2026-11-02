# Jaemin Kim — personal website

Ph.D. Researcher · Wireless networks, O-RAN, and online learning

Website: https://jmkim-jay.github.io/

## Editing

This is a static website with no framework or package dependencies.

- `scripts/build.py`: page layout, biography, research, news, and experience.
- `data/publications.json`: publication records and paper links.
- `assets/style.css`: responsive layout and visual style.
- `assets/site.js`: publication search and category filters.
- `assets/portrait.jpeg`: profile photo.

After editing content, regenerate the pages using Python 3:

```sh
python3 scripts/build.py
```

Commit both the source changes and the regenerated `index.html` / `publications.html`. The pages work without JavaScript; enabling JavaScript adds publication filtering. Every link to a paper points to its original host; no publisher PDF is rehosted here.

## GitHub Pages

Publish from `main` → `/ (root)` in **Settings → Pages → Deploy from a branch**. The `.nojekyll` file keeps the HTML and assets unchanged. No custom Actions workflow is required.

## Content provenance

The portrait, education, and initial 63 publication records are based on [the UCLab profile](https://uclab.re.kr/jmkim.html), accessed on 2026-11-02. Publication wording and author order follow the profile. Biography, research interests, news, and experience are maintained in `scripts/build.py`.

Paper URLs remain on UCLab or IEEE Xplore and may change independently. Update `data/publications.json` if those links change. UCLab's `/publications/original/` PDFs require authentication; these are labeled “PDF (lab access)”. Where a public PDF is available, the page shows that instead of the restricted copy.
