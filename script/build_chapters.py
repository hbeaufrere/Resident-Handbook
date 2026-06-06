#!/usr/bin/env python3
"""Split the converted handbook markdown into Jekyll chapter pages.

Detects plain "Label:" or "**Label:**" category lines and promotes them to H3
so reader can see groupings. Also strips stray blockquote markers introduced by
pandoc on indented Word paragraphs. Chapters that have numbered H2 subsections
(currently chapters 3 and 5) are split into one child page per subsection so
the just-the-docs sidebar can expand them.
"""
import re
import shutil
from pathlib import Path

SRC = Path(".tmp/handbook.md")
OUT = Path("docs")
if OUT.exists():
    # Wipe stale child pages so renames don't leave orphans
    shutil.rmtree(OUT)
OUT.mkdir(exist_ok=True)

text = SRC.read_text()
lines = text.splitlines()

ANCHOR_RE = re.compile(r'<span id="[^"]*" class="anchor"></span>')
MARK_RE = re.compile(r'<span class="mark">([^<]*)</span>')

LABEL_RE = re.compile(r"^(?:\*\*)?([A-Z][A-Za-z0-9 ,()/\-’'&]+?:)(?:\*\*)?\s*$")
BOLD_HEADER_RE = re.compile(r"^\*\*([A-Z][A-Za-z0-9 ,()/\-’'&.]+?)\*\*\s*$")
BLOCKQUOTE_PREFIX_RE = re.compile(r"^>\s?")

SUB_H2_RE = re.compile(r"^##\s+(\d+)\.(\d+)\s+(.+?)\s*$")

LEADING_NUM_RE = re.compile(r"^\s*\d+\.\s+\*\*[^*]+\*\*\s*$")
LEADING_APPENDIX_RE = re.compile(r"^\*\*APPENDIX[^*]+\*\*\s*$")
APPENDIX_H1_RE = re.compile(r"^#\s+APPENDIX[^\n]*$", re.IGNORECASE)
LEADING_H1_RE = re.compile(r"^#\s+\d+\.\s+", re.IGNORECASE)


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


def strip_leading_markers(body_lines):
    cleaned = [ANCHOR_RE.sub("", l) for l in body_lines]
    while cleaned and (
        LEADING_NUM_RE.match(cleaned[0])
        or LEADING_APPENDIX_RE.match(cleaned[0])
        or APPENDIX_H1_RE.match(cleaned[0])
        or LEADING_H1_RE.match(cleaned[0])
        or cleaned[0].strip() == ""
    ):
        cleaned.pop(0)
    return cleaned


def slugify(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9\s\-]", "", s).strip().lower()
    s = re.sub(r"[\s/_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s


def write_md(path: Path, front: dict, body: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    fm_lines = ["---"]
    for k, v in front.items():
        if isinstance(v, bool):
            fm_lines.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, int):
            fm_lines.append(f"{k}: {v}")
        else:
            fm_lines.append(f'{k}: "{v}"')
    fm_lines.append("---\n")
    path.write_text("\n".join(fm_lines) + "\n" + body)


chapters = [
    {"file": "chapter-01-members-contacts.md", "title": "1. Members & Contacts",
     "h1": "1. Companion Exotic Animal Medicine Members",
     "nav_order": 1, "start": 85, "end": 147, "split": False},
    {"file": "chapter-02-mentorship.md", "title": "2. House Officer Mentorship",
     "h1": "2. House Officer Mentorship", "nav_order": 2, "start": 147, "end": 153,
     "split": False},
    {"file": "chapter-03-research.md", "title": "3. Research Responsibilities",
     "h1": "3. Research Responsibilities — Residents", "nav_order": 3,
     "start": 153, "end": 193, "split": True, "folder": "chapter-03-research"},
    {"file": "chapter-04-teaching.md", "title": "4. Teaching Responsibilities",
     "h1": "4. Teaching Responsibilities", "nav_order": 4, "start": 193, "end": 215,
     "split": False},
    {"file": "chapter-05-clinical.md", "title": "5. Clinical Responsibilities",
     "h1": "5. Clinical Responsibilities", "nav_order": 5,
     "start": 215, "end": 708, "split": True, "folder": "chapter-05-clinical"},
    {"file": "chapter-06-professional-development.md",
     "title": "6. Professional Development", "h1": "6. Professional Development",
     "nav_order": 6, "start": 708, "end": 726, "split": False},
    {"file": "appendix-01-case-transfer-list.md",
     "title": "Appendix I — Case Transfer List",
     "h1": "Appendix I. Example Case Transfer List", "nav_order": 7,
     "start": 726, "end": 808, "split": False},
    {"file": "appendix-02-laboratory-notebooks.md",
     "title": "Appendix II — Laboratory Notebooks",
     "h1": "Appendix II. Policy and Procedures Related to Completion of Laboratory Notebooks",
     "nav_order": 8, "start": 808, "end": 923, "split": False},
    {"file": "appendix-03-special-animal-policies.md",
     "title": "Appendix III — Special Animal Policies",
     "h1": "Appendix III. Special Animal Policies", "nav_order": 9,
     "start": 923, "end": 1002, "split": False},
    {"file": "appendix-04-zoo-emergency.md",
     "title": "Appendix IV — Zoo Medicine Emergency Policy",
     "h1": "Appendix IV. Zoo Medicine Service Emergency Policy", "nav_order": 10,
     "start": 1002, "end": 1101, "split": False},
    {"file": "appendix-05-dates-to-know.md",
     "title": "Appendix V — Dates to Know",
     "h1": "Appendix V. Dates to Know", "nav_order": 11,
     "start": 1101, "end": None, "split": False},
]


def process_chapter(ch):
    start = ch["start"] - 1
    end = ch["end"] - 1 if ch["end"] else len(lines)
    body_lines = strip_leading_markers(lines[start:end])
    body_lines = promote_labels(body_lines)

    if not ch.get("split"):
        body = clean_block("\n".join(body_lines))
        write_md(
            OUT / ch["file"],
            {"title": ch["title"], "nav_order": ch["nav_order"]},
            f"# {ch['h1']}\n\n{body}",
        )
        print(f"  {ch['file']} ({len(body_lines)} lines)")
        return

    # Split: identify each ## X.Y subsection
    # Build a list of (line_index, chapter_num, sub_num, title)
    splits = []
    for i, ln in enumerate(body_lines):
        m = SUB_H2_RE.match(ln)
        if m:
            splits.append((i, int(m.group(1)), int(m.group(2)), m.group(3).strip()))

    if not splits:
        # No subsections detected — fall back to single page
        body = clean_block("\n".join(body_lines))
        write_md(
            OUT / ch["file"],
            {"title": ch["title"], "nav_order": ch["nav_order"]},
            f"# {ch['h1']}\n\n{body}",
        )
        return

    intro = clean_block("\n".join(body_lines[: splits[0][0]])) if splits[0][0] > 0 else ""

    # Parent page
    parent_front = {
        "title": ch["title"],
        "nav_order": ch["nav_order"],
        "has_children": True,
        "has_toc": True,
    }
    parent_body = f"# {ch['h1']}\n\n"
    if intro.strip():
        parent_body += intro + "\n"
    write_md(OUT / ch["file"], parent_front, parent_body)
    print(f"  {ch['file']} (parent, intro={len(intro)} chars, {len(splits)} children)")

    folder = OUT / ch["folder"]
    for idx, (line_i, cnum, snum, title) in enumerate(splits):
        next_i = splits[idx + 1][0] if idx + 1 < len(splits) else len(body_lines)
        # The subsection body starts AFTER the H2 line
        sub_lines = body_lines[line_i + 1 : next_i]
        sub_body = clean_block("\n".join(sub_lines))
        slug = slugify(title)[:60].strip("-")
        # Pad subsection numbers so 5.10 sorts after 5.9 in alphabetical file ordering
        filename = f"{cnum}-{snum:02d}-{slug}.md"
        nav_title = f"{cnum}.{snum} {title}"
        write_md(
            folder / filename,
            {
                "title": nav_title,
                "parent": ch["title"],
                "nav_order": snum,
            },
            f"# {cnum}.{snum} {title}\n\n{sub_body}",
        )
        print(f"    {ch['folder']}/{filename}")


print("Building chapter pages...")
for ch in chapters:
    process_chapter(ch)
print("done")
