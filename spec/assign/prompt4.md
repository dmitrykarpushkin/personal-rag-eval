You are writing part of a SYNTHETIC personal notebook (markdown files) for a fictional person, used as a public
benchmark corpus for retrieval-augmented search. Everything is fiction. Do not use real private people; the

Read the spec first: spec/world.yaml (persona, people, projects, layout, facts, forbidden).
Your planted notes: spec/assign/agent4.json — a map path -> list of facts that file
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

Your scope (4):
PERSONAL: inbox, journal, tasks, money (except invoices), family, mentoring. Planted files from agent4.json.
Filler (~110 files): journal/YYYY-MM-DD.md (about 45 days spread over Apr-Sep), inbox/YYYY-MM-DD-HHMM-<source>.md
(about 35 captures; about 10 in Russian, mostly family/Narva), tasks/YYYY-MM-DD-*.md (about 22, mix of open/done/dropped,
due dates spread; do NOT add other open tasks due 2026-10-01..2026-10-15 beyond the planted ones), money/taxes.md,
money/budget-2026-Q2.md, money/budget-2026-Q3.md, meetings/ (2 more mentoring calls with Oskar, 1 call with Hanna about
a job offer she pitched), mail/ (about 6: family, landlord, bank), people/oskar-nilsson.md, people/elin-lindqvist.md,
people/kadri-tamm.md, people/mart-rebane.md, people/hanna-kuusk.md. money/subscriptions.md must list the October renewals
exactly as planted and Savi €65 (raised from €55 in August); no other subscriptions renew in October.
