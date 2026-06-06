# Resident Handbook

Companion Exotic Animal Medicine and Surgery Service — House Officer Handbook,
published as a web ebook with GitHub Pages.

## View the handbook

Once GitHub Pages is enabled, the site is published at:

**https://hbeaufrere.github.io/resident-handbook/**

## Repository layout

```
.
├── _config.yml                   # Jekyll site config
├── Gemfile                       # Ruby dependencies (just-the-docs theme)
├── index.md                      # Cover / landing page
├── docs/                         # Chapter and appendix pages (markdown)
├── source/                       # Original .docx source document
└── .github/workflows/pages.yml   # Build & deploy to GitHub Pages
```

## Enabling GitHub Pages (one-time setup)

1. Go to **Settings → Pages** on the GitHub repo.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Push to `main` (or trigger the workflow from the Actions tab) — the
   `Build and deploy GitHub Pages` workflow will publish the site.

## Updating the handbook

### Small edits (typos, rewording, restructuring a section)

Edit the markdown files under `docs/` directly on GitHub:

1. Navigate to the file (e.g.
   `docs/chapter-05-clinical/5-04-referring-veterinarian-communication-responsibilities.md`).
2. Click the ✏ pencil icon → make your changes → **Commit changes**.
3. The `Build and deploy GitHub Pages` workflow rebuilds and redeploys
   automatically (~1–2 min, then ~5–10 min CDN flush).

### Wholesale revision from a new Word document

1. Replace `source/Resident Handbook *.docx` via the GitHub UI:
   open the `source/` folder → **Add file → Upload files** → drag in the
   new `.docx` → **Commit changes** (any filename ending in `.docx` works).
2. The workflow notices the `.docx` in the push, runs pandoc, re-runs
   `script/build_chapters.py`, commits the regenerated `docs/` back to
   the branch, then builds + deploys.

> Heads up: this step overwrites any direct markdown edits in `docs/`.
> If you've made hand edits since the last `.docx` upload, copy them
> over after the regenerate completes.

You can also force a regenerate without changing the `.docx`:
**Actions tab → Build and deploy GitHub Pages → Run workflow → check
"Regenerate docs/ from source/*.docx"**.

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>.
