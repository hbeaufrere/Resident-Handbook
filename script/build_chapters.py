#!/usr/bin/env python3
"""Split the converted handbook markdown into Jekyll chapter pages.

Detects plain "Label:" or "**Label:**" category lines and promotes them to H3
so reader can see groupings. Also strips stray blockquote markers introduced by
pandoc on indented Word paragraphs.
"""
import re
from pathlib import Path

SRC = Path(".tmp/handbook.md")
OUT = Path("docs")
OUT.mkdir(exist_ok=True)

text = SRC.read_text()
lines = text.splitlines()

ANCHOR_RE = re.compile(r'<span id="[^"]*" class="anchor"></span>')
MARK_RE = re.compile(r'<span class="mark">([^<]*)</span>')

# A short label paragraph: optionally bolded, ends with colon, < 90 chars.
LABEL_RE = re.compile(r"^(?:\*\*)?([A-Z][A-Za-z0-9 ,()/\-’'&]+?:)(?:\*\*)?\s*$")
# A short bold-only header (no colon), used in appendices like "**Grant Preproposal Deadlines**"
BOLD_HEADER_RE = re.compile(r"^\*\*([A-Z][A-Za-z0-9 ,()/\-’'&.]+?)\*\*\s*$")
# Pandoc blockquote prefix introduced from indented Word paragraphs
BLOCKQUOTE_PREFIX_RE = re.compile(r"^>\s?")


def clean_block(block: str) -> str:
    block = ANCHOR_RE.sub("", block)
    block = MARK_RE.sub(r"\1", block)
    block = re.sub(r"\n{3,}", "\n\n", block)
    return block.strip() + "\n"


def promote_labels(body_lines):
    out = []
    n = len(body_lines)

    def adj_nonempty(i, step):
        j = i + step
        while 0 <= j < n and body_lines[j].strip() == "":
            j += step
        return body_lines[j] if 0 <= j < n else ""

    def near_form_field(idx):
        for nbr in (adj_nonempty(idx, 1), adj_nonempty(idx, -1)):
            if nbr.strip().count("_") >= 8:
                return True
        return False

    for i, ln in enumerate(body_lines):
        stripped_bq = BLOCKQUOTE_PREFIX_RE.sub("", ln)
        if stripped_bq != ln:
            ln = stripped_bq
        m = LABEL_RE.match(ln)
        if m and len(ln) < 60 and len(m.group(1).split()) <= 8 and not near_form_field(i):
            out.append(f"### {m.group(1)}")
            continue
        m2 = BOLD_HEADER_RE.match(ln)
        if m2:
            txt = m2.group(1).strip()
            if (
                len(txt) < 70
                and len(txt.split()) <= 7
                and txt[-1] not in ".!?"
                and not near_form_field(i)
            ):
                out.append(f"### {txt}")
                continue
        out.append(ln)
    return out


LEADING_NUM_RE = re.compile(r"^\s*\d+\.\s+\*\*[^*]+\*\*\s*$")
LEADING_APPENDIX_RE = re.compile(r"^\*\*APPENDIX[^*]+\*\*\s*$")
APPENDIX_H1_RE = re.compile(r"^#\s+APPENDIX[^\n]*$", re.IGNORECASE)
LEADING_H1_RE = re.compile(r"^#\s+\d+\.\s+", re.IGNORECASE)

chapters = [
    {"file": "chapter-01-members-contacts.md", "title": "1. Members & Contacts",
     "h1": "1. Companion Exotic Animal Medicine Members and related contact information",
     "nav_order": 1, "start": 85, "end": 147},
    {"file": "chapter-02-mentorship.md", "title": "2. House Officer Mentorship",
     "h1": "2. House Officer Mentorship", "nav_order": 2, "start": 147, "end": 153},
    {"file": "chapter-03-research.md", "title": "3. Research Responsibilities",
     "h1": "3. Research Responsibilities — Residents", "nav_order": 3,
     "start": 153, "end": 193},
    {"file": "chapter-04-teaching.md", "title": "4. Teaching Responsibilities",
     "h1": "4. Teaching Responsibilities", "nav_order": 4, "start": 193, "end": 215},
    {"file": "chapter-05-clinical.md", "title": "5. Clinical Responsibilities",
     "h1": "5. Clinical Responsibilities", "nav_order": 5, "start": 215, "end": 708},
    {"file": "chapter-06-professional-development.md",
     "title": "6. Professional Development", "h1": "6. Professional Development",
     "nav_order": 6, "start": 708, "end": 726},
    {"file": "appendix-01-case-transfer-list.md",
     "title": "Appendix I — Case Transfer List",
     "h1": "Appendix I. Example Case Transfer List", "nav_order": 7,
     "start": 726, "end": 808},
    {"file": "appendix-02-laboratory-notebooks.md",
     "title": "Appendix II — Laboratory Notebooks",
     "h1": "Appendix II. Policy and Procedures Related to Completion of Laboratory Notebooks",
     "nav_order": 8, "start": 808, "end": 923},
    {"file": "appendix-03-special-animal-policies.md",
     "title": "Appendix III — Special Animal Policies",
     "h1": "Appendix III. Special Animal Policies", "nav_order": 9,
     "start": 923, "end": 1002},
    {"file": "appendix-04-zoo-emergency.md",
     "title": "Appendix IV — Zoo Medicine Emergency Policy",
     "h1": "Appendix IV. Zoo Medicine Service Emergency Policy", "nav_order": 10,
     "start": 1002, "end": 1101},
    {"file": "appendix-05-dates-to-know.md",
     "title": "Appendix V — Dates to Know",
     "h1": "Appendix V. Dates to Know", "nav_order": 11,
     "start": 1101, "end": None},
]

for ch in chapters:
    start = ch["start"] - 1
    end = ch["end"] - 1 if ch["end"] else len(lines)
    body_lines = lines[start:end]
    cleaned_lines = [ANCHOR_RE.sub("", l) for l in body_lines]

    while cleaned_lines and (
        LEADING_NUM_RE.match(cleaned_lines[0])
        or LEADING_APPENDIX_RE.match(cleaned_lines[0])
        or APPENDIX_H1_RE.match(cleaned_lines[0])
        or LEADING_H1_RE.match(cleaned_lines[0])
        or cleaned_lines[0].strip() == ""
    ):
        cleaned_lines.pop(0)

    cleaned_lines = promote_labels(cleaned_lines)

    body = "\n".join(cleaned_lines)
    body = clean_block(body)

    front = (
        "---\n"
        f"title: \"{ch['title']}\"\n"
        f"nav_order: {ch['nav_order']}\n"
        "---\n\n"
        f"# {ch['h1']}\n\n"
    )
    (OUT / ch["file"]).write_text(front + body)
    print(f"wrote {ch['file']} ({len(cleaned_lines)} lines)")

print("done")
