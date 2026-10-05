| retriever | hit@1 | hit@5, 95% CI | recall@5 | recall@10 | MRR, 95% CI | median ms |
|---|---|---|---|---|---|---|
| hybrid | 0.57 | 0.86 [0.80–0.93] | 0.81 | 0.90 | 0.71 [0.64–0.77] | 150 |
| hybrid+mq | 0.61 | 0.91 [0.86–0.95] | 0.86 | 0.90 | 0.75 [0.68–0.81] | 600 |

hit@5 by question type:

| retriever | aggregate (n=11) | crosslingual (n=11) | identifier (n=6) | lookup (n=34) | multihop (n=8) | paraphrase (n=23) | temporal (n=18) |
|---|---|---|---|---|---|---|---|
| hybrid | 0.91 | 0.82 | 1.00 | 0.97 | 1.00 | 0.70 | 0.78 |
| hybrid+mq | 1.00 | 0.91 | 1.00 | 1.00 | 0.88 | 0.83 | 0.78 |
