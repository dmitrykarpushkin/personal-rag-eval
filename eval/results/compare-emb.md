## dense: e5-base vs e5-large

Paired comparison: dense@e5-base vs dense@e5-large (95% bootstrap intervals over questions; * = the interval excludes 0)

### all answerable (n=111)

| metric | dense@e5-large | dense@e5-base | dense@e5-base − dense@e5-large |
|---|---|---|---|
| hit@5 | 0.87 [0.81–0.93] | 0.77 [0.69–0.85] | -0.10 [-0.17, -0.03] * |
| mrr | 0.69 [0.62–0.76] | 0.61 [0.53–0.68] | -0.08 [-0.15, -0.02] * |

First gold rank changed: A03 1→18, I01 3→1, I04 3→10, L01 1→3, L03 5→4, L05 1→4, L07 2→1, L10 2→6, L14 4→1, M01 3→1, P01 1→3, P02 7→12, P03 31→None, P05 22→35, P07 16→4, S05 1→2, S06 1→5, S07 5→1, S08 2→1, S12 3→1, S13 4→1, S17 1→5, S18 1→6, S22 28→None, S24 6→31, S25 1→2, S26 2→23, S27 1→4, S28 2→3, S29 1→2, S31 1→2, S34 3→38, S35 31→13, S36 4→9, S37 7→9, S39 20→25, S40 8→4, S42 5→9, S43 42→None, S44 2→4, S46 12→7, S48 1→2, S50 4→16, S52 5→4, S53 12→31, S54 1→2, S55 1→6, S56 10→1, S59 3→7, S60 5→16, T01 2→6, T05 1→4, T06 1→2, T08 2→3, T10 2→4, X01 1→3, X02 5→2, X03 4→6, X05 1→3

### temporal (n=18)

| metric | dense@e5-large | dense@e5-base | dense@e5-base − dense@e5-large |
|---|---|---|---|
| hit@5 | 0.78 [0.56–0.94] | 0.67 [0.44–0.89] | -0.11 [-0.33, +0.11] |
| mrr | 0.53 [0.36–0.70] | 0.41 [0.26–0.58] | -0.12 [-0.23, -0.03] * |

First gold rank changed: S36 4→9, S37 7→9, S39 20→25, S40 8→4, S42 5→9, S43 42→None, T01 2→6, T05 1→4, T06 1→2, T08 2→3, T10 2→4

### asks for the current value (n=14)

| metric | dense@e5-large | dense@e5-base | dense@e5-base − dense@e5-large |
|---|---|---|---|
| hit@5 | 0.86 [0.64–1.00] | 0.71 [0.50–0.93] | -0.14 [-0.36, +0.00] |
| mrr | 0.64 [0.45–0.84] | 0.47 [0.28–0.67] | -0.18 [-0.31, -0.06] * |

First gold rank changed: S31 1→2, S39 20→25, S42 5→9, S43 42→None, T01 2→6, T05 1→4, T06 1→2, T10 2→4

## dense: bge-m3 vs e5-large

Paired comparison: dense@bge-m3 vs dense@e5-large (95% bootstrap intervals over questions; * = the interval excludes 0)

### all answerable (n=111)

| metric | dense@e5-large | dense@bge-m3 | dense@bge-m3 − dense@e5-large |
|---|---|---|---|
| hit@5 | 0.87 [0.81–0.93] | 0.85 [0.77–0.91] | -0.03 [-0.09, +0.04] |
| mrr | 0.69 [0.62–0.76] | 0.65 [0.58–0.72] | -0.04 [-0.09, +0.02] |

First gold rank changed: A03 1→12, I01 3→1, I04 3→4, I06 1→2, L03 5→4, L05 1→2, L07 2→5, L09 1→3, L10 2→3, L12 2→1, L14 4→3, P02 7→3, P03 31→19, P04 4→7, P05 22→9, P07 16→4, P08 1→2, S07 5→3, S12 3→1, S22 28→14, S24 6→4, S25 1→3, S26 2→4, S27 1→2, S28 2→1, S29 1→2, S34 3→2, S35 31→17, S36 4→15, S37 7→16, S39 20→12, S40 8→1, S43 42→25, S44 2→3, S45 1→3, S46 12→14, S48 1→2, S49 1→2, S50 4→9, S52 5→1, S53 12→16, S56 10→1, S57 1→2, S58 1→6, S59 3→9, S60 5→10, T04 4→17, T06 1→2, T07 1→2, T08 2→1, T10 2→4, X02 5→2, X03 4→2

### temporal (n=18)

| metric | dense@e5-large | dense@bge-m3 | dense@bge-m3 − dense@e5-large |
|---|---|---|---|
| hit@5 | 0.78 [0.56–0.94] | 0.72 [0.50–0.89] | -0.06 [-0.22, +0.11] |
| mrr | 0.53 [0.36–0.70] | 0.51 [0.34–0.69] | -0.02 [-0.14, +0.13] |

First gold rank changed: S36 4→15, S37 7→16, S39 20→12, S40 8→1, S43 42→25, T04 4→17, T06 1→2, T07 1→2, T08 2→1, T10 2→4

### asks for the current value (n=14)

| metric | dense@e5-large | dense@bge-m3 | dense@bge-m3 − dense@e5-large |
|---|---|---|---|
| hit@5 | 0.86 [0.64–1.00] | 0.79 [0.57–1.00] | -0.07 [-0.21, +0.00] |
| mrr | 0.64 [0.45–0.84] | 0.55 [0.35–0.74] | -0.10 [-0.20, -0.01] * |

First gold rank changed: S39 20→12, S43 42→25, T04 4→17, T06 1→2, T07 1→2, T10 2→4

## hybrid: e5-base vs e5-large

Paired comparison: hybrid@e5-base vs hybrid@e5-large (95% bootstrap intervals over questions; * = the interval excludes 0)

### all answerable (n=111)

| metric | hybrid@e5-large | hybrid@e5-base | hybrid@e5-base − hybrid@e5-large |
|---|---|---|---|
| hit@5 | 0.86 [0.80–0.93] | 0.81 [0.74–0.88] | -0.05 [-0.12, +0.01] |
| mrr | 0.71 [0.64–0.77] | 0.64 [0.57–0.71] | -0.07 [-0.11, -0.02] * |

First gold rank changed: A03 1→7, I04 3→8, L03 6→5, L05 1→2, L10 2→3, L14 2→1, P02 8→15, P03 33→None, P05 11→10, P07 18→5, S06 1→4, S07 2→1, S12 2→1, S13 2→1, S15 2→1, S17 1→4, S22 7→21, S24 7→48, S25 1→2, S26 3→27, S27 2→4, S28 2→3, S29 1→2, S34 4→None, S35 27→13, S36 4→8, S39 13→15, S42 6→9, S43 12→13, S44 3→7, S45 1→3, S46 7→4, S48 1→2, S50 4→15, S52 6→5, S53 13→40, S54 1→2, S55 3→8, S56 2→1, S59 2→4, S60 4→17, T01 1→3, T02 2→1, T04 2→3, T06 1→2, T07 2→3, T10 3→2, X01 3→4, X02 5→2, X03 4→6, X05 1→5, X06 1→3

### temporal (n=18)

| metric | hybrid@e5-large | hybrid@e5-base | hybrid@e5-base − hybrid@e5-large |
|---|---|---|---|
| hit@5 | 0.78 [0.56–0.94] | 0.72 [0.50–0.89] | -0.06 [-0.17, +0.00] |
| mrr | 0.54 [0.38–0.71] | 0.49 [0.33–0.65] | -0.06 [-0.17, +0.05] |

First gold rank changed: S36 4→8, S39 13→15, S42 6→9, S43 12→13, T01 1→3, T02 2→1, T04 2→3, T06 1→2, T07 2→3, T10 3→2

### asks for the current value (n=14)

| metric | hybrid@e5-large | hybrid@e5-base | hybrid@e5-base − hybrid@e5-large |
|---|---|---|---|
| hit@5 | 0.79 [0.57–1.00] | 0.79 [0.57–1.00] | +0.00 [+0.00, +0.00] |
| mrr | 0.65 [0.46–0.84] | 0.55 [0.37–0.74] | -0.10 [-0.22, -0.00] * |

First gold rank changed: S39 13→15, S42 6→9, S43 12→13, T01 1→3, T04 2→3, T06 1→2, T07 2→3, T10 3→2

## hybrid: bge-m3 vs e5-large

Paired comparison: hybrid@bge-m3 vs hybrid@e5-large (95% bootstrap intervals over questions; * = the interval excludes 0)

### all answerable (n=111)

| metric | hybrid@e5-large | hybrid@bge-m3 | hybrid@bge-m3 − hybrid@e5-large |
|---|---|---|---|
| hit@5 | 0.86 [0.80–0.93] | 0.86 [0.80–0.93] | +0.00 [-0.06, +0.06] |
| mrr | 0.71 [0.64–0.77] | 0.70 [0.63–0.77] | -0.00 [-0.05, +0.05] |

First gold rank changed: A03 1→3, I04 3→5, L03 6→4, L07 2→7, L14 2→1, M01 1→2, P02 8→5, P03 33→20, P04 2→3, P05 11→4, P07 18→6, S12 2→1, S13 2→3, S15 2→1, S22 7→5, S24 7→4, S25 1→5, S26 3→6, S27 2→3, S28 2→1, S29 1→2, S34 4→3, S35 27→18, S36 4→10, S37 9→21, S39 13→8, S40 4→2, S42 6→5, S43 12→6, S44 3→4, S45 1→3, S46 7→14, S47 2→3, S48 1→2, S50 4→9, S52 6→1, S53 13→16, S55 3→1, S56 2→1, S58 1→2, S59 2→6, S60 4→9, T02 2→1, T04 2→11, T06 1→2, T07 2→3, T08 2→1, T10 3→1, X02 5→2, X03 4→2

### temporal (n=18)

| metric | hybrid@e5-large | hybrid@bge-m3 | hybrid@bge-m3 − hybrid@e5-large |
|---|---|---|---|
| hit@5 | 0.78 [0.56–0.94] | 0.72 [0.50–0.89] | -0.06 [-0.22, +0.11] |
| mrr | 0.54 [0.38–0.71] | 0.59 [0.41–0.76] | +0.04 [-0.08, +0.18] |

First gold rank changed: S36 4→10, S37 9→21, S39 13→8, S40 4→2, S42 6→5, S43 12→6, T02 2→1, T04 2→11, T06 1→2, T07 2→3, T08 2→1, T10 3→1

### asks for the current value (n=14)

| metric | hybrid@e5-large | hybrid@bge-m3 | hybrid@bge-m3 − hybrid@e5-large |
|---|---|---|---|
| hit@5 | 0.79 [0.57–1.00] | 0.79 [0.57–1.00] | +0.00 [-0.21, +0.21] |
| mrr | 0.65 [0.46–0.84] | 0.64 [0.44–0.83] | -0.02 [-0.15, +0.12] |

First gold rank changed: S39 13→8, S42 6→5, S43 12→6, T04 2→11, T06 1→2, T07 2→3, T10 3→1

