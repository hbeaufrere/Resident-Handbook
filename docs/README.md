# Where the handbook text lives

Each page of the website is one markdown file in this folder. Edit the file,
commit, and the site rebuilds automatically.

**Chapters with subsections (3 and 5) are split into a folder.** The top-level
`chapter-03-research.md` / `chapter-05-clinical.md` files contain only the
chapter heading — the text is in the matching folder, one file per subsection.

| Section | Edit this file |
|---|---|
| Cover / home page | `../index.md` |
| 1. Members & Contacts | `chapter-01-members-contacts.md` |
| 2. House Officer Mentorship | `chapter-02-mentorship.md` |
| 3. Research Responsibilities | *(heading only)* `chapter-03-research.md` |
| &nbsp;&nbsp;3.1 Scientific Publications and Presentations | `chapter-03-research/3-01-scientific-publications-and-presentations.md` |
| &nbsp;&nbsp;3.2 Original Research | `chapter-03-research/3-02-original-research.md` |
| &nbsp;&nbsp;3.3 Case Reports | `chapter-03-research/3-03-case-reports.md` |
| 4. Teaching Responsibilities | `chapter-04-teaching.md` |
| 5. Clinical Responsibilities | *(heading only)* `chapter-05-clinical.md` |
| &nbsp;&nbsp;5.1 Professional Relations | `chapter-05-clinical/5-01-professional-relations.md` |
| &nbsp;&nbsp;5.2 Clinic schedule | `chapter-05-clinical/5-02-clinic-schedule.md` |
| &nbsp;&nbsp;5.3 Client Communication Responsibilities | `chapter-05-clinical/5-03-client-communication-responsibilities.md` |
| &nbsp;&nbsp;5.4 Referring Veterinarian Communication Responsibilities | `chapter-05-clinical/5-04-referring-veterinarian-communication-responsibilities.md` |
| &nbsp;&nbsp;5.5 Phones | `chapter-05-clinical/5-05-phones.md` |
| &nbsp;&nbsp;5.6 In Patient Care Responsibilities | `chapter-05-clinical/5-06-in-patient-care-responsibilities.md` |
| &nbsp;&nbsp;5.7 Controlled Drugs | `chapter-05-clinical/5-07-controlled-drugs.md` |
| &nbsp;&nbsp;5.8 Daily Organization/Scheduling Responsibilities | `chapter-05-clinical/5-08-daily-organizationscheduling-responsibilities.md` |
| &nbsp;&nbsp;5.9 Ongoing clinical research | `chapter-05-clinical/5-09-ongoing-clinical-research.md` |
| &nbsp;&nbsp;5.10 Responsibilities for Medical Records | `chapter-05-clinical/5-10-responsibilities-for-medical-records.md` |
| &nbsp;&nbsp;5.11 Rounds | `chapter-05-clinical/5-11-rounds.md` |
| &nbsp;&nbsp;5.12 Service Meetings | `chapter-05-clinical/5-12-service-meetings.md` |
| &nbsp;&nbsp;5.13 On Call Emergency Responsibilities | `chapter-05-clinical/5-13-on-call-emergency-responsibilities.md` |
| &nbsp;&nbsp;5.14 Patient Charges | `chapter-05-clinical/5-14-patient-charges.md` |
| &nbsp;&nbsp;5.15 Additional Responsibilities – AAH, CRC, MGZ | `chapter-05-clinical/5-15-additional-responsibilities-aahcrcmgz.md` |
| &nbsp;&nbsp;5.16 California Raptor Center (CRC) | `chapter-05-clinical/5-16-responsibilities-for-the-california-raptor-center-crc.md` |
| &nbsp;&nbsp;5.17 Aquatic Animal Health (AAH) | `chapter-05-clinical/5-17-responsibilities-on-aquatic-animal-health-aah.md` |
| &nbsp;&nbsp;5.18 Micke Grove Zoo (MGZ) | `chapter-05-clinical/5-18-responsibilities-for-the-micke-grove-zoo-mgz.md` |
| &nbsp;&nbsp;5.19 Off-Site Rotations – Residents | `chapter-05-clinical/5-19-off-site-rotations-residents.md` |
| &nbsp;&nbsp;5.20 Case Transfers When Rotating Off Clinics | `chapter-05-clinical/5-20-case-transfers-when-rotating-off-clinics.md` |
| &nbsp;&nbsp;5.21 Moonlighting | `chapter-05-clinical/5-21-moonlighting.md` |
| &nbsp;&nbsp;5.22 Planning ahead for post-program interviews | `chapter-05-clinical/5-22-planning-ahead-for-post-program-interviews.md` |
| 6. Professional Development | `chapter-06-professional-development.md` |
| Appendix I — Case Transfer List | `appendix-01-case-transfer-list.md` |
| Appendix II — Laboratory Notebooks | `appendix-02-laboratory-notebooks.md` |
| Appendix III — Special Animal Policies | `appendix-03-special-animal-policies.md` |
| Appendix IV — Zoo Medicine Emergency Policy | `appendix-04-zoo-emergency.md` |
| Appendix V — Dates to Know | `appendix-05-dates-to-know.md` |

## Anatomy of a page file

```markdown
---
title: "5.4 Referring Veterinarian Communication Responsibilities"   ← sidebar label
parent: "5. Clinical Responsibilities"                                ← which chapter it sits under
nav_order: 4                                                          ← order within the chapter
---

# 5.4 Referring Veterinarian Communication Responsibilities          ← page heading

Body text in Markdown. **bold**, *italic*, numbered lists (1. 2. 3.),
bullet lists (- item), links [text](https://…).
```

Leave the block between the `---` lines alone unless you're renaming or
reordering a page. Everything below the heading is the editable text.

## Adding a new subsection to chapter 5

Create `chapter-05-clinical/5-23-your-title.md` with the same front-matter
shape as above (`parent: "5. Clinical Responsibilities"`, `nav_order: 23`).
It appears in the sidebar and in the chapter's table of contents automatically.

## Regenerating everything from a new Word file

Upload a new `.docx` to `../source/` — the GitHub Actions workflow re-splits
it into these files. **That overwrites any hand edits made here**, so fold your
edits into the Word document first, or re-apply them afterwards.
