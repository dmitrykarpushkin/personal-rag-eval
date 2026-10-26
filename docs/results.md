# Results

Back to the [README](../README.md). Every raw answer and retrieval row is in [eval/results/](../eval/results/).


## Answers (end to end, 119 questions)

333-note notebook (`corpus/`), answering model Claude Sonnet 5.5 unless marked `@haiku`:

| system | correct, 95% CI | answerable correct | right "not found" on unanswerable | cites a gold note | median input tokens | mean cost $ |
|---|---|---|---|---|---|---|
| agent+search | **0.99** [0.97–1.00] | 0.99 | 1.00 | 0.99 | 25,152 | 0.029 |
| agentic-grep | 0.98 [0.96–1.00] | 0.98 | 1.00 | 0.97 | 36,367 | 0.040 |
| full-context | 1.00 [1.00–1.00] | 1.00 | 1.00 | 0.99 | 102,600 | 0.031 |
| rag:hybrid+rerank | 0.92 [0.87–0.97] | 0.93 | 0.88 | 0.92 | 8,606 | 0.017 |
| rag:hybrid | 0.87 [0.82–0.93] | 0.86 | 1.00 | 0.87 | 8,298 | 0.015 |
| rag:dense | 0.87 [0.82–0.93] | 0.87 | 0.88 | 0.89 | 8,371 | 0.016 |
| full-context@haiku | 0.99 [0.98–1.00], 3 runs | 0.99 | 1.00 | 0.97 | 75,003 | 0.014 |
| agentic-grep@haiku | 0.92 [0.87–0.96], 3 runs | 0.95 | 0.50 | 0.90 | 29,668 | 0.026 |
| rag:hybrid@haiku | 0.87 [0.81–0.93] | 0.86 | 1.00 | 0.83 | 10,575 | 0.009 |

Intervals are 95% percentile bootstrap over questions ([`eval/stats.py`](../eval/stats.py)). Against agentic grep on
the same questions (paired bootstrap), every one-shot RAG variant is worse with the interval excluding zero
(rag:hybrid −0.11 [−0.17, −0.05], rag:hybrid+rerank −0.06 [−0.12, −0.01]); agent+search (+0.01 [−0.02, +0.04])
and the whole notebook in context (+0.02 [+0.00, +0.04]) are not distinguishable from it on 119 questions.

Run-to-run noise, three identical runs: agentic-grep@haiku 0.924 / 0.924 / 0.916, with 5% of questions flipping
between right and wrong; full-context@haiku 0.992 in all three, 1.7% flipping. So differences of one or two
points between agent setups are within noise; the gap to one-shot RAG is not. Rows with 3 runs are pooled over
the runs.

1,138-note notebook (`corpus/` + `archive/`, the same questions):

| system | correct | median input tokens | mean cost $ |
|---|---|---|---|
| agent+search | 0.98 | 25,087 | 0.034 |
| agentic-grep | 0.99 | 43,109 | 0.044 |
| full-context | 0.99 | 269,976 | 0.087 |
| rag:hybrid+rerank | 0.91 | 9,658 | 0.017 |
| rag:hybrid | 0.83 | 9,321 | 0.016 |

Breakdowns by question type are in [`eval/results/answers.md`](../eval/results/answers.md) and
[`eval/results/answers-xl.md`](../eval/results/answers-xl.md).

## Retrieval only (111 answerable questions, note-level)

| retriever | hit@1 | hit@5 | recall@5 | MRR | median latency |
|---|---|---|---|---|---|
| grep (keyword count) | 0.33 | 0.61 | 0.58 | 0.46 | 2 ms |
| BM25 in Postgres | 0.41 | 0.63 | 0.60 | 0.52 | 5 ms |
| dense (pgvector, e5-large) | 0.57 | 0.87 | 0.82 | 0.69 | 142 ms |
| hybrid, RRF | 0.45 | 0.77 | 0.70 | 0.59 | 146 ms |
| hybrid, convex 0.7 | 0.57 | 0.87 | 0.82 | 0.71 | 147 ms |
| hybrid + bge-reranker-v2-m3 | **0.67** | **0.89** | **0.86** | **0.76** | 9.4 s (CPU) |

hit@5 by question type, and the same table for the large notebook, are in
[`eval/results/retrieval.md`](../eval/results/retrieval.md) and
[`eval/results/retrieval-xl.md`](../eval/results/retrieval-xl.md).

## Date-aware retrieval

Notes go stale: the March note and the July note both match "what is my hourly rate", and plain relevance ranks
them about the same. `hybrid+dates` ([`src/prag/dates.py`](../src/prag/dates.py)) adds two things on top of the
convex hybrid:

- **date filters** `since` / `until` on the chunk date (front matter `created`, else a date in the file name, else,
  with `PRAG_DATE_FROM_MTIME=1`, the file's modification time);
- **a recency term**: score = (1 − w)·relevance + w·2^(−age / half-life), applied in `auto` mode only to questions
  that ask for the current, latest or final value (a small EN/RU keyword detector). Settings:
  `PRAG_RECENCY=off|auto|always`, `PRAG_RECENCY_WEIGHT` (w = 0.3), `PRAG_RECENCY_HALF_LIFE_DAYS` (90), `PRAG_TODAY`.
  The defaults were set before the run, not tuned on the gold set.

Paired comparison with the plain hybrid on the same index (eval date 2026-09-30; * = the interval excludes 0):

| questions | hit@5 hybrid → +dates | difference | MRR difference |
|---|---|---|---|
| all answerable (111) | 0.86 → 0.88 | +0.02 [0.00, +0.05] | +0.01 [0.00, +0.02] * |
| temporal (18) | 0.78 → 0.89 | +0.11 [0.00, +0.28] | +0.05 [+0.01, +0.11] * |
| flagged as "current value" (14) | 0.79 → 0.93 | +0.14 [0.00, +0.36] | +0.06 [+0.01, +0.14] * |

In `auto` mode only 4 questions change rank and all improve; nothing gets worse. With recency on every question
(`always`, a control run) temporal questions gain a little more, but ordinary lookups lose (one gold note drops
from rank 6 to 12, another from 11 to 23), which is why `auto` is the default. Details:
[`eval/results/compare-dates.md`](../eval/results/compare-dates.md),
[`eval/results/compare-dates-always.md`](../eval/results/compare-dates-always.md).

## Embedding models

Does the 560M-parameter e5-large earn its cost? The same corpus is indexed three times, once per embedder, each in
its own database (`PRAG_DSN`, `PRAG_EMBED_MODEL`, `PRAG_EMBED_DIM`). The E5 query/passage prefixes are kept for E5
models only. BM25 and the fusion weight (0.7) stay the same. All three runs use the current corpus, so the e5-large
row can differ by a point from the table above.

| embedder | dims | dense hit@5 | dense MRR | hybrid hit@5 | hybrid MRR | median query ms |
|---|---|---|---|---|---|---|
| multilingual-e5-large | 1024 | 0.87 [0.81–0.93] | 0.69 | 0.86 [0.80–0.93] | 0.71 | 125 |
| multilingual-e5-base | 768 | 0.77 [0.69–0.85] | 0.61 | 0.81 [0.74–0.88] | 0.64 | 43 |
| bge-m3 | 1024 | 0.85 [0.77–0.91] | 0.65 | 0.86 [0.80–0.93] | 0.70 | 135 |

Paired against e5-large on the same 111 questions (* = the interval excludes 0):

- **e5-base is clearly worse.** Dense: hit@5 −0.10 [−0.17, −0.03] *, MRR −0.08 [−0.15, −0.02] *. Hybrid:
  hit@5 −0.05 [−0.12, +0.01], MRR −0.07 [−0.11, −0.02] *. BM25 recovers about half of the hit@5 loss. In exchange, queries
  are 2.6–2.9× faster on CPU (median 47 vs 124 ms hybrid, 43 vs 125 ms dense).
- **bge-m3 matches e5-large inside hybrid search.** Hybrid: hit@5 +0.00 [−0.06, +0.06], MRR −0.00 [−0.05, +0.05].
  Dense alone is slightly behind: hit@5 −0.03 [−0.09, +0.04], MRR −0.04 [−0.09, +0.02], neither significant. The
  question types differ: bge-m3 is better on paraphrases (hybrid 0.83 vs 0.70) and worse on multi-hop questions
  (0.75 vs 1.00). With 8 to 23 questions per type, these per-type differences are not significant.

Indexing the 518 chunks took 63 s with e5-base and 168 s with bge-m3. e5-large was not re-indexed for this run.
Details: [`eval/results/retrieval-emb.md`](../eval/results/retrieval-emb.md),
[`eval/results/compare-emb.md`](../eval/results/compare-emb.md); reproduce with `eval/compare_embeddings.py`.

## Multi-query

`hybrid+mq` ([`src/prag/multiquery.py`](../src/prag/multiquery.py)): Claude Haiku 4.5 rewrites the question into 3
search queries (other wording, the kind of note, at least one in the other language). The convex hybrid search runs
for the question and each rewrite, and the scores are summed per chunk. The number of rewrites and the fusion rule
were fixed before the run. Rewrites are cached ([`eval/results/rewrites.jsonl`](../eval/results/rewrites.jsonl), made
by `eval/make_rewrites.py`), so the retrieval numbers are repeatable.

Paired comparison with the plain hybrid on the same index and the same 111 questions (* = the interval excludes 0):

| questions | hit@5 hybrid → +mq | difference | MRR difference |
|---|---|---|---|
| all answerable (111) | 0.86 → 0.91 | +0.05 [0.00, +0.10] | +0.04 [0.00, +0.09] |
| temporal (18) | 0.78 → 0.78 | +0.00 [−0.17, +0.17] | −0.02 [−0.13, +0.08] |
| flagged as "current value" (14) | 0.79 → 0.86 | +0.07 [0.00, +0.21] | −0.03 [−0.15, +0.10] |

Seven questions enter the top 5 and two drop out. The gains are on paraphrased questions (hit@5 0.70 → 0.83),
cross-language questions (0.82 → 0.91) and aggregates (0.91 → 1.00). Multi-hop questions lose one (1.00 → 0.88).
The overall gain sits right at the edge of significance on 111 questions. What it costs: about 10 s of model time
per question (median, before caching), $0.006 per question at list prices, and 4× the search time (median 600 vs
150 ms, four hybrid searches). Details: [`eval/results/retrieval-mq.md`](../eval/results/retrieval-mq.md),
[`eval/results/compare-mq.md`](../eval/results/compare-mq.md).

