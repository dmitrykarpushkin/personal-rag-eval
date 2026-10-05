| retriever | hit@1 | hit@5, 95% CI | recall@5 | recall@10 | MRR, 95% CI | median ms |
|---|---|---|---|---|---|---|
| dense | 0.48 | 0.77 [0.69–0.85] | 0.74 | 0.84 | 0.61 [0.53–0.68] | 43 |
| hybrid | 0.51 | 0.81 [0.74–0.88] | 0.78 | 0.86 | 0.64 [0.57–0.71] | 47 |

hit@5 by question type:

| retriever | aggregate (n=11) | crosslingual (n=11) | identifier (n=6) | lookup (n=34) | multihop (n=8) | paraphrase (n=23) | temporal (n=18) |
|---|---|---|---|---|---|---|---|
| dense | 0.73 | 0.73 | 0.83 | 0.94 | 0.75 | 0.65 | 0.67 |
| hybrid | 0.73 | 0.73 | 0.83 | 1.00 | 0.88 | 0.65 | 0.72 |
