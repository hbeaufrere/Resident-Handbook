#!/usr/bin/env bash
# Builds downloadable handbook artifacts (epub + docx copy) into assets/downloads/.
# Run before `jekyll build` so Jekyll copies the artifacts into _site/.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

OUT="assets/downloads"
mkdir -p "$OUT"

# Copy the source .docx (renamed to a stable, URL-friendly filename)
DOCX_SRC=$(ls source/*.docx 2>/dev/null | head -1 || true)
if [[ -n "$DOCX_SRC" ]]; then
  cp "$DOCX_SRC" "$OUT/resident-handbook.docx"
  echo "Copied $DOCX_SRC -> $OUT/resident-handbook.docx"
else
  echo "No source .docx found in source/" >&2
fi

# Concatenate chapter markdown for pandoc (strip Jekyll front matter)
TMP_MD="$(mktemp)"
trap 'rm -f "$TMP_MD"' EXIT

{
  echo "% House Officer Handbook"
  echo "% Companion Exotic Animal Medicine and Surgery Service, UC Davis"
  echo "% Updated 05/2026"
  echo
  for f in \
    docs/chapter-01-members-contacts.md \
    docs/chapter-02-mentorship.md \
    docs/chapter-03-research.md \
    docs/chapter-04-teaching.md \
    docs/chapter-05-clinical.md \
    docs/chapter-06-professional-development.md \
    docs/appendix-01-case-transfer-list.md \
    docs/appendix-02-laboratory-notebooks.md \
    docs/appendix-03-special-animal-policies.md \
    docs/appendix-04-zoo-emergency.md \
    docs/appendix-05-dates-to-know.md
  do
    # Strip the leading YAML front matter, keep the body
    awk 'BEGIN{fm=0} /^---$/{fm++; next} fm>=2{print}' "$f"
    echo
  done
} > "$TMP_MD"

# Build EPUB
if command -v pandoc >/dev/null 2>&1; then
  pandoc "$TMP_MD" \
    --from=gfm \
    --to=epub \
    --metadata title="House Officer Handbook" \
    --metadata author="UC Davis VMTH — Companion Exotic Animal Medicine and Surgery Service" \
    --metadata date="2026-05" \
    --toc --toc-depth=2 \
    -o "$OUT/resident-handbook.epub"
  echo "Built $OUT/resident-handbook.epub"
else
  echo "pandoc not installed; skipping epub" >&2
fi
