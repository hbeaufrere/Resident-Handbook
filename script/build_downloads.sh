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

# Enumerate chapter and appendix pages in reading order. For chapters that
# were split into per-subsection child pages (chapters 3 and 5), pull each
# child file in numeric order *instead of* the parent stub.
list_pages() {
  for stem in \
    chapter-01-members-contacts \
    chapter-02-mentorship \
    chapter-03-research \
    chapter-04-teaching \
    chapter-05-clinical \
    chapter-06-professional-development \
    appendix-01-case-transfer-list \
    appendix-02-laboratory-notebooks \
    appendix-03-special-animal-policies \
    appendix-04-zoo-emergency \
    appendix-05-dates-to-know
  do
    if [[ -d "docs/$stem" ]]; then
      # split chapter: include parent then children sorted by filename
      echo "docs/$stem.md"
      find "docs/$stem" -name "*.md" | LC_ALL=C sort
    else
      echo "docs/$stem.md"
    fi
  done
}

{
  echo "% House Officer Handbook"
  echo "% Companion Exotic Animal Medicine and Surgery Service, UC Davis"
  echo "% Updated 05/2026"
  echo
  while IFS= read -r f; do
    # Strip the leading YAML front matter, keep the body
    awk 'BEGIN{fm=0} /^---$/{fm++; next} fm>=2{print}' "$f"
    echo
  done < <(list_pages)
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
