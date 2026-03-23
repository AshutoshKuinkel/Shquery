Core functionality:
PR created → Spin up a very short lived postgres container → apply ddl queries from repo migrations e.g. create table.. → Scan codebase for SQL queries → Run EXPLAIN on each one → Flag anything with Seq Scan and high cost → Leave comment on pr

Change model -> 

Add a workload simulation using golang for this aswell

E.g.:
Seq Scan on 1M rows? → flag it
Missing index on WHERE column? → flag it
Cost jumped vs previous PR? → flag it

ML:

1. Regression Detection, i.e. comparing EXPLAIN output across PRs over time. If cost_total for a query keeps creeping up across commits, that's a regression even if no single PR looks obviously bad. A model can spot that trend better than a static threshold.

2. Optimisation suggestions, i.e. learning from your codebase's history. "Every query on this table that had a Seq Scan and then got an index added saw X% improvement" → proactively suggest the same fix on new queries.

---

Update: New way to go about this...
User Spins up integration tests
Spin up ephermal db
We'll have to use OTEL (generates and expors telemetry (traces, metrics, logs) from your code)
Then we get structure our RAW SQL we get from OTEL in a json with db.statement etc... and run EXPLAIN/EXPLAIN ANALYZE on it
Run workload sims etc..
Handle ML regression logic
Leave comment on pr
