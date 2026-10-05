| retriever | hit@1 | hit@5, 95% CI | recall@5 | recall@10 | MRR, 95% CI | median ms |
|---|---|---|---|---|---|---|
| dense | 0.57 | 0.87 [0.81–0.93] | 0.82 | 0.88 | 0.69 [0.62–0.76] | 125 |
| hybrid | 0.57 | 0.86 [0.80–0.93] | 0.81 | 0.90 | 0.71 [0.64–0.77] | 124 |

hit@5 by question type:

| retriever | aggregate (n=11) | crosslingual (n=11) | identifier (n=6) | lookup (n=34) | multihop (n=8) | paraphrase (n=23) | temporal (n=18) |
|---|---|---|---|---|---|---|---|
| dense | 0.91 | 0.91 | 1.00 | 1.00 | 0.88 | 0.70 | 0.78 |
| hybrid | 0.91 | 0.82 | 1.00 | 0.97 | 1.00 | 0.70 | 0.78 |
