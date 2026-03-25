Core functionality:
PR created → Spin up a very short lived postgres container with logging enabled → run integration/e2e tests → capture SQL queries @ run time→ Run EXPLAIN ANALYZE on each one → Flag anything with Seq Scan and high cost → RUN workload sims → ML regression calculation/optimisation suggestions → Leave comment on pr → shut down the short lived db and everything

Add a workload simulation using golang for this aswell

E.g.:
Seq Scan on 1M rows? → flag it
Cost jumped vs previous PR? → flag it

ML:

1. Regression Detection, i.e. comparing EXPLAIN output across PRs over time. If cost_total for a query keeps creeping up across commits, that's a regression even if no single PR looks obviously bad. A model can spot that trend better than a static threshold.

2. Optimisation suggestions, i.e. learning from your codebase's history. "Every query on this table that had a Seq Scan and then got an index added saw X% improvement" → proactively suggest the same fix on new queries.

Core limitation: Coverage of tool is directly proportional to the coverage of integeration/e2e tests... Codebases with greater coverage, especially on non-trivial APIs, naturally are more likely to benefit from tool. Maybe, there is a way I can efficeintly combine a static extraction of queries in codebase (without having to maintain different parser for each language) with this postgreSQL json logging to increase coverage. However, this is a task for later. Core functionality with limitation is first priority.
---
