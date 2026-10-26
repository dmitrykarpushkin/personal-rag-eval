# personal-rag-eval

**English** · [Русский](README.ru.md)

[![CI](https://github.com/dmitrykarpushkin/personal-rag-eval/actions/workflows/ci.yml/badge.svg)](https://github.com/dmitrykarpushkin/personal-rag-eval/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**How should an AI assistant search one person's notes? Classic RAG loses to an agent that searches for itself.**

A reproducible benchmark for anyone building an assistant over private notes: four ways to answer questions
about a bilingual (English + Russian) notebook, graded on 119 questions with confidence intervals and cost per
answer. Scoring is mechanical, no LLM judge.

![Correct answers and cost per question](docs/accuracy-cost.svg)

## What it found

- **One-shot RAG is the weakest way to answer.** Its best version (hybrid search + reranker) gets 92% right; an
  agent that greps the folder itself gets 98%, the whole notebook in the prompt gets 100%. When retrieval misses,
  one-shot RAG has nothing else to try.
- **Give the agent a search tool: same accuracy, 27% cheaper.** With a hybrid `search_notes` tool the agent scores
  99%, reads 31% fewer tokens and takes fewer steps than with grep alone.
- **The gap grows with the notebook.** At 3.4x the notes, grep costs 18% more tokens, the search tool stays flat,
  and the whole-notebook prompt costs 2.8x as much. Around 4,000 notes it no longer fits a 1M context.
- **Semantic search does the heavy lifting.** Keyword grep finds the right note in the top 5 for 61% of questions,
  hybrid search with a reranker for 89%; on questions asked in the other language, 9% vs 100%.
- **Plain RRF fusion made hybrid search worse than dense alone.** A weighted sum of normalised scores fixed it.

## The four approaches

333-note notebook, answering model Claude Sonnet 5.5, 95% bootstrap intervals over questions:

| | Correct | Median input tokens | Mean cost per answer |
|---|---|---|---|
| One-shot RAG (hybrid + reranker) | 0.92 [0.87–0.97] | 8,606 | $0.017 |
| Agent with grep | 0.98 [0.96–1.00] | 36,367 | $0.040 |
| **Agent with grep + search tool** | **0.99** [0.97–1.00] | 25,152 | $0.029 |
| Whole notebook in the prompt | 1.00 [1.00–1.00] | 102,600 | $0.031 |

Against the grep agent on the same questions, every one-shot RAG variant is worse with the interval excluding
zero; the search-tool agent and the whole notebook are not distinguishable from it on 119 questions. All tables,
the 1,138-note run, date-aware retrieval, embedding models and multi-query: [docs/results.md](docs/results.md).

![Input tokens per question as the notebook grows](docs/tokens-scale.svg)

## Quick start

The unit tests need no database or models:

```bash
git clone https://github.com/dmitrykarpushkin/personal-rag-eval && cd personal-rag-eval
pip install numpy pyyaml pytest && pytest -q
```

The full run needs Docker (Postgres 16 + pgvector) and, for the answer evals, a logged-in `claude` CLI:
`pip install -e . && docker compose up -d --wait && make index goldset eval-retrieval`. All steps: [docs/method.md](docs/method.md).

## How it works

- **Retrieval in plain Postgres:** BM25 computed in SQL, pgvector for dense search, a weighted fusion and an
  optional cross-encoder reranker. Embeddings and reranker run locally on the CPU; no paid APIs in the retrieval path.
- **The same search as an MCP tool,** so any agent can use it next to Grep and Read.
- **A fictional notebook built to be hard:** 333 notes over six months (plus 805 older ones for the scaling run),
  generated from a [world spec](spec/world.yaml) that plants each fact next to stale values and near misses.
- **Gold set:** 59 hand-written and 60 synthetic questions across eight types (lookup, paraphrase, temporal,
  identifier, aggregate, cross-lingual, multi-hop, unanswerable). An answer counts when its regexes match;
  "not found" counts only on unanswerable questions.

Architecture diagram, benchmark design and every reproduction command: [docs/method.md](docs/method.md).

## Limitations

The corpus is synthetic and written by LLMs; real notes are messier. 119 questions give wide intervals (one
question is 0.8 points), and most systems were run once; repeated runs show agent setups flip on about 2-5% of
questions, so one or two points between them is noise, the gap to one-shot RAG is not. Costs are API list prices
reported by Claude Code, for comparison only.

---

License: [MIT](LICENSE) · Author: [Dmitry Karpushkin](https://github.com/dmitrykarpushkin) ·
Every person, company and event in the corpus is fictional.
