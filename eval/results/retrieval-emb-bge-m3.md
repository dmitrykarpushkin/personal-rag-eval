| retriever | hit@1 | hit@5, 95% CI | recall@5 | recall@10 | MRR, 95% CI | median ms |
|---|---|---|---|---|---|---|
| dense | 0.50 | 0.85 [0.77–0.91] | 0.81 | 0.87 | 0.65 [0.58–0.72] | 135 |
| hybrid | 0.59 | 0.86 [0.80–0.93] | 0.83 | 0.92 | 0.70 [0.64–0.77] | 141 |

hit@5 by question type:

| retriever | aggregate (n=11) | crosslingual (n=11) | identifier (n=6) | lookup (n=34) | multihop (n=8) | paraphrase (n=23) | temporal (n=18) |
|---|---|---|---|---|---|---|---|
| dense | 0.73 | 0.91 | 1.00 | 1.00 | 0.62 | 0.78 | 0.72 |
| hybrid | 0.82 | 0.91 | 1.00 | 0.97 | 0.75 | 0.83 | 0.72 |
