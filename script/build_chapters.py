#!/usr/bin/env python3
"""Split the converted handbook markdown into Jekyll chapter pages."""
import re
import os
from pathlib import Path

SRC = Path(".tmp/handbook.md")
OUT = Path("docs")
OUT.mkdir(exist_ok=True)

text = SRC.read_text()
lines = text.splitlines()

# Cleanup helpers
ANCHOR_RE = re.compile(r'<span id="[^"]*" class="anchor"></span>')
MARK_RE = re.compile(r'<span class="mark">([^<]*)</span>')

def clean(block: str) -> str:
    block = ANCHOR_RE.sub("", block)
    block = MARK_RE.sub(r"\1", block)
    # Collapse 3+ blank lines
    block = re.sub(r"\n{3,}", "\n\n", block)
    return block.strip() + "\n"

# Slice ranges are (start_line_1indexed, end_line_1indexed_exclusive_or_None)
chapters = [
    {
        "file": "chapter-01-members-contacts.md",
        "title": "1. Members & Contacts",
        "h1": "1. Companion Exotic Animal Medicine Members and related contact information",
        "nav_order": 1,
        "start": 85, "end": 147,
    },
    {
        "file": "chapter-02-mentorship.md",
        "title": "2. House Officer Mentorship",
        "h1": "2. House Officer Mentorship",
        "nav_order": 2,
        "start": 147, "end": 153,
    },
    {
        "file": "chapter-03-research.md",
        "title": "3. Research Responsibilities",
        "h1": "3. Research Responsibilities — Residents",
        "nav_order": 3,
        "start": 153, "end": 193,
    },
    {
        "file": "chapter-04-teaching.md",
        "title": "4. Teaching Responsibilities",
        "h1": "4. Teaching Responsibilities",
        "nav_order": 4,
        "start": 193, "end": 215,
    },
    {
        "file": "chapter-05-clinical.md",
        "title": "5. Clinical Responsibilities",
        "h1": "5. Clinical Responsibilities",
        "nav_order": 5,
        "start": 215, "end": 708,
    },
    {
        "file": "chapter-06-professional-development.md",
        "title": "6. Professional Development",
        "h1": "6. Professional Development",
        "nav_order": 6,
        "start": 708, "end": 726,
    },
    {
        "file": "appendix-01-case-transfer-list.md",
        "title": "Appendix I — Case Transfer List",
        "h1": "Appendix I. Example Case Transfer List",
        "nav_order": 7,
        "start": 726, "end": 808,
    },
    {
        "file": "appendix-02-laboratory-notebooks.md",
        "title": "Appendix II — Laboratory Notebooks",
        "h1": "Appendix II. Policy and Procedures Related to Completion of Laboratory Notebooks",
        "nav_order": 8,
        "start": 808, "end": 923,
    },
    {
        "file": "appendix-03-special-animal-policies.md",
        "title": "Appendix III — Special Animal Policies",
        "h1": "Appendix III. Special Animal Policies",
        "nav_order": 9,
        "start": 923, "end": 1002,
    },
    {
        "file": "appendix-04-zoo-emergency.md",
        "title": "Appendix IV — Zoo Medicine Emergency Policy",
        "h1": "Appendix IV. Zoo Medicine Service Emergency Policy",
        "nav_order": 10,
        "start": 1002, "end": 1101,
    },
    {
        "file": "appendix-05-dates-to-know.md",
        "title": "Appendix V — Dates to Know",
        "h1": "Appendix V. Dates to Know",
        "nav_order": 11,
        "start": 1101, "end": None,
    },
]

# Strip the original first-line markers like "1.  **TITLE**" / "**APPENDIX I. ..."
LEADING_NUM_RE = re.compile(r"^\s*\d+\.\s+\*\*[^*]+\*\*\s*$")
LEADING_APPENDIX_RE = re.compile(r"^\*\*APPENDIX[^*]+\*\*\s*$")
APPENDIX_H1_RE = re.compile(r"^#\s+APPENDIX[^\n]*$", re.IGNORECASE)
LEADING_H1_RE = re.compile(r"^#\s+\d+\.\s+", re.IGNORECASE)

for ch in chapters:
    start = ch["start"] - 1
    end = ch["end"] - 1 if ch["end"] else len(lines)
    body_lines = lines[start:end]

    # Pre-clean each line so the leading-marker regex can match
    cleaned_lines = [ANCHOR_RE.sub("", l) for l in body_lines]

    # Drop the first line if it's the auto-numbered chapter marker or appendix h1
    while cleaned_lines and (
        LEADING_NUM_RE.match(cleaned_lines[0])
        or LEADING_APPENDIX_RE.match(cleaned_lines[0])
        or APPENDIX_H1_RE.match(cleaned_lines[0])
        or LEADING_H1_RE.match(cleaned_lines[0])
        or cleaned_lines[0].strip() == ""
    ):
        cleaned_lines.pop(0)

    body = "\n".join(cleaned_lines)
    body = clean(body)

    front = (
        "---\n"
        f"title: \"{ch['title']}\"\n"
        f"nav_order: {ch['nav_order']}\n"
        "---\n\n"
        f"# {ch['h1']}\n\n"
    )
    (OUT / ch["file"]).write_text(front + body)
    print(f"wrote {ch['file']} ({len(body_lines)} lines)")

print("done")
