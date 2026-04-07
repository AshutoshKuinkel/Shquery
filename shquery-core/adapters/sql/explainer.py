# purpose: run EXPLAIN to receive quick & efficient cost plan on queries. Frontline checking before workload sim.
'''
TO DO: Write up module docstring
'''

import parser;
from dotenv import load_dotenv
import os
load_dotenv()

# approach: loop through the final dictonary returned from build_query_stats() 
# and run EXPLAIN on it to get cost plan:
query_dict = parser.build_query_stats(os.getenv("JSONL_FILE_PATH"))

# loop through just the query keys, it's fine to run it on all queries. just a simple EXPLAIN, either way
# O(N)..
# return dict output, 
# with cost plan for that query (reference it with the hash we created in tallied_queries function )
# TO DO: see how this fits in with workload sims, to determine if dict output is right way to go..

for query in query_dict.values():
  query = query['query']
  
  # TO DO: Run explain on these queries
