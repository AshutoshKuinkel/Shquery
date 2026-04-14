'''
This module is responsible for efficeintly retrieving COST PLANS for SQL queries.
It runs on the SQL queries collected and stored using parser module. The 
COST/EXECUTION PLANS are gathered using the EXPLAIN keyword in sql.

The main purpose of this module in the workflow is to help alert developers on 
queries that may potentially be problematic in their own workflows, i.e. catch
sequential scans when no index present etc. This tool doesn't strictly serve as a
guard pointing to a query and saying this query is bad, instead it finds potential
problematic queries and alerts the developer. This module assists us in acheiving
this goal quickly and efficiently, acting as a frontline check before the workload
simulations (designed to reveal issues under load).

A drawback is that the tooling assumes integration tests are similar and mostly mirror
queries in production. The efficiency of the tooling is directly proportonial to
the amount of integration,e2e etc.. tests featured. It is also not 100% guaranteed to 
catch all queries that could cause problems in real-world software.

TO DO: MENTION APPROACH...
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
