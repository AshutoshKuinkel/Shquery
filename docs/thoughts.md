

Right, so getting db.statement with jest is kinda funky.. it's not showing me db.statements for queries with jest..

Dug depper on this like 2 nights ago for some hours and turns out root cause is jest worker isolation combined with multiple SDK instances overwriting global tracer provider.

So essientially:
--require ./tests/tracing.js runs in the main Jest process, SDK starts, pg gets patched, global tracer provider registered
Jest then spawns multiple worker processes (one per test file) using jest-worker
Each worker also runs --require ./tests/tracing.js (because --require propagates to child processes)
Each worker calls sdk.start() which re-registers a new global tracer provider, overwriting the previous one
You end up with multiple SDK instances all competing for the same global — the last one to register wins
When pg queries run, they create spans against whichever tracer provider is currently registered globally, but the SimpleSpanProcessor/ConsoleSpanExporter attached to that specific SDK instance may not be the one that's actually active anymore
Net result: spans are created but never reach an exporter

This is why the smoke script works perfectly, single process, single SDK instance, no workers, no collision.


I may have to run jaeger or something like this, maybe only way I can get it working...

---

Forget about all this... using PostgreSQL json logging finally worked to fetch all queries at runtime... now just need to parse,normalise,run explain analyse, workloads sims + ML....

---

thought: set would be good for deduplication, as we avoid having exact same query more than once, also note set is basically dict w/out the keys, so still O(1) lookups..
Im thinking maybe we could store in dict, then deduplicate by storing in set, then add to dict again, or maybe just add to a set right away..
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This isn't a worry,
