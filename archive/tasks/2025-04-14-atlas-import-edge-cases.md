---
created: 2025-04-14T12:51:00
source: note
tags: [task, work, lumen, atlas-import]
status: done
due: 2025-04-25
---
# Atlas import edge cases

List all the CSV edge cases for Atlas import with support: Excel quote styles, semicolon delimiters, BOM. Done, 14 cases, the BOM one was the worst.

Sat with support for an hour and listed every CSV that had broken an import: semicolon delimiters, quote styles from different Excel versions, byte-order marks, dates in three formats, empty trailing columns. The BOM issue alone explained a dozen tickets. Fourteen cases total, each with a sample file.
