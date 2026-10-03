| system | accuracy (all), 95% CI | answerable correct | says "not found" when it should | wrongly says "not found" | cites a gold note | median s | median input tokens | mean cost $ |
|---|---|---|---|---|---|---|---|---|
| agentic-grep | 0.99 [0.97–1.00] (n=119) | 0.99 | 1.00 | 0.00 | 0.97 | 10.8 | 43,109 | 0.044 |
| agent+search | 0.98 [0.96–1.00] (n=119) | 0.98 | 1.00 | 0.00 | 0.96 | 7.6 | 25,087 | 0.034 |
| full-context | 0.99 [0.97–1.00] (n=119) | 1.00 | 0.88 | 0.00 | 1.00 | 5.4 | 269,976 | 0.087 |
| rag:hybrid | 0.83 [0.76–0.90] (n=119) | 0.83 | 0.88 | 0.08 | 0.81 | 4.3 | 9,321 | 0.016 |
| rag:hybrid+rerank | 0.91 [0.85–0.96] (n=119) | 0.90 | 1.00 | 0.03 | 0.86 | 17.5 | 9,658 | 0.017 |

Paired difference in accuracy vs agentic-grep (same questions, 95% bootstrap CI; * = the interval excludes 0):

| system | difference | questions |
|---|---|---|
| agent+search | -0.01 [-0.04, +0.02] | 119 |
| full-context | +0.00 [-0.03, +0.03] | 119 |
| rag:hybrid | -0.16 [-0.23, -0.09] * | 119 |
| rag:hybrid+rerank | -0.08 [-0.14, -0.03] * | 119 |

Accuracy by question type:

| system | aggregate (n=11) | crosslingual (n=11) | identifier (n=6) | lookup (n=34) | multihop (n=8) | paraphrase (n=23) | temporal (n=18) | unanswerable (n=8) |
|---|---|---|---|---|---|---|---|---|
| agentic-grep | 0.91 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| agent+search | 0.91 | 1.00 | 1.00 | 0.97 | 1.00 | 1.00 | 1.00 | 1.00 |
| full-context | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.88 |
| rag:hybrid | 0.73 | 0.64 | 1.00 | 0.97 | 0.75 | 0.74 | 0.83 | 0.88 |
| rag:hybrid+rerank | 0.82 | 0.82 | 1.00 | 1.00 | 0.88 | 0.83 | 0.89 | 1.00 |
