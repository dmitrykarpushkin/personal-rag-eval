| system | accuracy (all), 95% CI | answerable correct | says "not found" when it should | wrongly says "not found" | cites a gold note | median s | median input tokens | mean cost $ |
|---|---|---|---|---|---|---|---|---|
| agentic-grep | 0.98 [0.96–1.00] (n=119) | 0.98 | 1.00 | 0.01 | 0.97 | 9.1 | 36,367 | 0.040 |
| agent+search | 0.99 [0.97–1.00] (n=119) | 0.99 | 1.00 | 0.00 | 0.99 | 7.3 | 25,152 | 0.029 |
| full-context | 1.00 [1.00–1.00] (n=119) | 1.00 | 1.00 | 0.00 | 0.99 | 5.0 | 102,600 | 0.031 |
| rag:dense | 0.87 [0.82–0.93] (n=119) | 0.87 | 0.88 | 0.06 | 0.89 | 4.0 | 8,371 | 0.016 |
| rag:hybrid | 0.87 [0.82–0.93] (n=119) | 0.86 | 1.00 | 0.05 | 0.87 | 4.0 | 8,298 | 0.015 |
| rag:hybrid+rerank | 0.92 [0.87–0.97] (n=119) | 0.93 | 0.88 | 0.01 | 0.92 | 14.9 | 8,606 | 0.017 |
| rag:hybrid@haiku | 0.87 [0.81–0.93] (n=119) | 0.86 | 1.00 | 0.05 | 0.83 | 8.2 | 10,575 | 0.009 |
| agentic-grep@haiku | 0.92 [0.87–0.97] (n=119) | 0.95 | 0.62 | 0.01 | 0.86 | 11.0 | 54,901 | 0.024 |
| full-context@haiku | 0.99 [0.97–1.00] (n=119) | 0.99 | 1.00 | 0.00 | 0.95 | 8.4 | 83,903 | 0.020 |

Paired difference in accuracy vs agentic-grep (same questions, 95% bootstrap CI; * = the interval excludes 0):

| system | difference | questions |
|---|---|---|
| agent+search | +0.01 [-0.02, +0.04] | 119 |
| full-context | +0.02 [+0.00, +0.04] | 119 |
| rag:dense | -0.11 [-0.17, -0.05] * | 119 |
| rag:hybrid | -0.11 [-0.17, -0.05] * | 119 |
| rag:hybrid+rerank | -0.06 [-0.12, -0.01] * | 119 |
| rag:hybrid@haiku | -0.11 [-0.18, -0.05] * | 119 |
| agentic-grep@haiku | -0.06 [-0.11, -0.02] * | 119 |
| full-context@haiku | +0.01 [-0.02, +0.04] | 119 |

Accuracy by question type:

| system | aggregate (n=11) | crosslingual (n=11) | identifier (n=6) | lookup (n=34) | multihop (n=8) | paraphrase (n=23) | temporal (n=18) | unanswerable (n=8) |
|---|---|---|---|---|---|---|---|---|
| agentic-grep | 1.00 | 0.91 | 1.00 | 1.00 | 1.00 | 1.00 | 0.94 | 1.00 |
| agent+search | 0.91 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| full-context | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| rag:dense | 0.73 | 0.91 | 1.00 | 1.00 | 0.75 | 0.83 | 0.78 | 0.88 |
| rag:hybrid | 0.82 | 0.82 | 1.00 | 1.00 | 0.75 | 0.74 | 0.83 | 1.00 |
| rag:hybrid+rerank | 0.91 | 1.00 | 1.00 | 1.00 | 0.75 | 0.83 | 0.94 | 0.88 |
| rag:hybrid@haiku | 0.64 | 0.82 | 1.00 | 1.00 | 0.62 | 0.83 | 0.89 | 1.00 |
| agentic-grep@haiku | 0.82 | 0.73 | 1.00 | 1.00 | 1.00 | 0.96 | 1.00 | 0.62 |
| full-context@haiku | 0.91 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
