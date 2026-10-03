---
created: 2024-05-24T09:38:00
source: note
tags: [lumen, design]
---
# Beacon score: how it is built

Short design note I keep for the team.

Score = weighted sum of five signals: usage trend, breadth of features used, last contact age, open support tickets, contract renewal proximity. Each signal is normalised to 0-100 and weights are set per segment.

Why not machine learning: no labelled churn history, small data, and CS needs to explain the number to a customer. If we get a year of labelled outcomes we can try a model and compare against this one as a baseline.

Known weakness: new accounts. They get a grey chip until 14 days of data exist.
