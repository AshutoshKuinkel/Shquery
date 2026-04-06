# purpose: run EXPLAIN to receive quick & efficient cost plan on queries. Frontline checking before workload sim.
# references:
import parser;

# approach: loop through the final dictonary returned from build_query_stats() 
# and run EXPLAIN on it to get cost plan:
query_dict = parser.build_query_stats()

# loop through just the query keys here, it's fine to run it on all queries. just a simple EXPLAIN, either way
# O(N)..

# return dict output, 
# with cost plan for that query (reference it with the hash we created in tallied_queries function )
# TO DO: see how this fits in with workload sims, to determine if dict output is right way to go..
