You are writing part of a SYNTHETIC personal notebook (markdown files) for a fictional person, used as a public
benchmark corpus for retrieval-augmented search. Everything is fiction. Do not use real private people; the

Read the spec first: spec/world.yaml (persona, people, projects, layout, facts, forbidden).
Your planted notes: spec/assign/agent1.json — a map path -> list of facts that file
MUST contain (role "gold" = the correct/current answer; role "distractors" = an older or near-miss value that must
appear in that file as described). Write files under corpus/<path>.

Rules
1. Every planted file must state its must_contain content clearly and exactly (same numbers, dates, names, IDs,
   spelling), embedded naturally in a realistic note — not as a Q&A. Never copy the benchmark question text.
   Where must_contain says IN RUSSIAN, write that note in Russian.
2. Then write FILLER notes for your scope (below) to make the notebook realistic and *hard*: same people and
   projects mentioned many times, similar topics, near-duplicate vocabulary, progress logs, small decisions,
   chit-chat, todo fragments. Filler must NOT contradict any fact in world.yaml, must NOT state any alternative
   value for a planted fact (no other rates, dates, prices, IDs for the same things), and must respect `forbidden`.
   Filler may mention planted facts only in a way that agrees with the CURRENT (gold) value and only if dated after it,
   or simply refer to the topic without the value ("talked to Rui about the flat").
3. Every file starts with YAML frontmatter: created (ISO datetime within 2026-04-01..2026-09-30, consistent with the
   filename date), source (one of: note, voice, chat, email, web, journal), tags (list). Tasks also have status and
   optional due. Then markdown body. Vary length: 40–700 words, mostly 120–350. Vary style: terse bullets, rambling
   journal, meeting summary, email digest with quoted lines.
4. Only create files inside your scope. Do not touch other agents' paths. Use realistic filenames per layout.
5. Mara writes mostly in English; Russian for family matters and some voice memos (about 1 in 4 inbox voice memos).
6. When done, reply with one line: number of files written and total words (run `find ... | xargs wc -w`).

Your scope (1):
WORK / Harbor. Planted files from agent1.json. Filler (~60 files): projects/harbor/YYYY-MM-DD-*.md dated logs
(sprints, standups, incidents, decisions, retro notes, about 30), meetings/YYYY-MM-DD-harbor-*.md (weekly syncs with
Priya, design reviews with Jon Ahlberg, one architecture review with Tomasz; about 15), mail/YYYY-MM-DD-*.md email digests
about Harbor (about 10), people/priya-raman.md, people/jon-ahlberg.md. Harbor ticket ids look like HRB-<number>; use
other HRB numbers freely but never HRB-212 or HRB-121 outside the planted files. Do not create invoices other than the
planted ones.
