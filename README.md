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

Edit the markdown files under `docs/` and commit. The Actions workflow will
rebuild and republish automatically.

To regenerate the chapter pages from a new `.docx` revision, see the helper
script `script/build_chapters.py` (run after dropping the new doc in `source/`).

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>.
