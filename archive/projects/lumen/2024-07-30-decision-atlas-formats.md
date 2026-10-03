---
created: 2024-07-30T10:12:00
source: note
tags: [lumen, decision]
---
# Decision: Which file formats Atlas will accept at launch

CSV and TSV at launch, xlsx later. Reasons: 90% of customers upload CSV, xlsx adds sheet and merged cell problems, and nobody wants to maintain a parser for formats we will not support well. Encoding: UTF-8, UTF-16 and Windows-1257 sniffed automatically. Kertu agreed, xlsx moves to Q4.
