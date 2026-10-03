---
created: 2024-08-12T17:32:00
source: note
tags: [lumen, design]
---
# Atlas: the ten errors users hit most

From beta logs and support tickets, in order of frequency:
1. wrong file type (xlsx renamed to csv)
2. header row missing
3. date in two formats in one column
4. decimal comma interpreted as thousand separator
5. duplicate key
6. required column empty
7. encoding not UTF-8
8. extra delimiter inside a quoted field
9. file empty
10. file too large

For each, a plain sentence and a fix. Triin will use this for the support guide.
