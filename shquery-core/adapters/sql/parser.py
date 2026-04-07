# purpose: extract clean queries from json file
# references: 
# https://www.geeksforgeeks.org/python/read-json-file-using-python
# https://www.geeksforgeeks.org/python/json-loads-in-python
# DDL VS DML: https://www.geeksforgeeks.org/dbms/difference-between-ddl-and-dml-in-dbms
# MD5: https://www.geeksforgeeks.org/python/md5-hash-python/
'''
  TO DO: Write module docstring
'''

import json;
import os
import hashlib;
from dotenv import load_dotenv
load_dotenv()

# TO DO: figure out how to determine what makes 2 queries same for deduplication, i.e. SELECT * FROM users where id=123 & SELECT * FROM users where id=456

# approach:
# filter to catch sql queries only (deduplication/normalisation included), load into dict w/ hash, query & count (count could help identifying hot queries/what to optimise etc..)...
# then run EXPLAIN for costs plan... 

DDL_WORDS = {'create', 'alter', 'drop', 'truncate', 'comment', 'rename'}
  
def extract_raw_sql_queries(json_lines_file_path:str)-> list[str]:
  """
  Extract SQL queries from JSONL ( `JSON-Lines <https://jsonltools.com/what-is-jsonl>`_) log file.

  Args:
    json_lines_file_path (string): (Path to the JSONL log file.)
    
  Returns:
        list[str]: Raw SQL strings, unfiltered and uncleaned.
  """
  queries = []
  try:
    with open(json_lines_file_path,'r') as file:
      for line in file:
        try:
          py_obj_query = json.loads(line)
        except json.JSONDecodeError:
          # more suitable to throw continue here instead of JSONDecodeErr, so whole pipeline doesn't break.
          continue  
        
        query = py_obj_query.get('message','')
        if query.startswith('execute'):
          sql = query.split(":", 1)[1]
          queries.append(sql)
        else:
          continue
  except FileNotFoundError:
    raise FileNotFoundError(f"{json_lines_file_path} not found!")
  
  return queries;  
  
def normalise_and_filter(queries: list[str]) -> list[str]:
  '''
    Normalise whitespace, lowercase, & filter out DDL statements.
    
    Args:
      queries (list[str]): Raw SQL strings.

    Returns:
      list[str]: Cleaned DML-only SQL strings.
  '''
  clean_queries = []
  
  for q in queries:
    sql = " ".join(q.split()).lower()
    
    if sql.split()[0] in DDL_WORDS:
      continue
    
    clean_queries.append(sql)
    
  return clean_queries
  
def tallied_queries(clean_queries: list[str]) -> dict:
  '''
    Process each normalised/filtered query to include hash,count and final query before passing to EXPLAIN.
    
    Args:
      queries (list[str]): Cleaned DML-only SQL strings.
      
    Returns:
      dict: Keyed by short hash, each value containing:
            - 'sql' (str): The normalised SQL query
            - 'count' (int): Execution frequency
            - 'hash' (str): Short hash for referencing in reports

  '''
  processed_queries = {}
  
  for query in clean_queries:
    
    # hash query + store in hex form for readability/cleanliness:
    hashed_query = hashlib.md5(query.encode()).hexdigest()[:8]
    
    
    if hashed_query in processed_queries:
      processed_queries[hashed_query]['count'] += 1
    else:
      processed_queries[hashed_query] = {
        "hash" : hashed_query,
        "query" : query,
        "count" : 1
      }
      
  return processed_queries
  
def build_query_stats(path: str) -> dict:
    """
    Full pipeline: extract, normalise, finalise.

    Args:
        path (str): Path to the JSONL log file.

    Returns:
        dict: Deduplicated query store with counts.
    """
    raw = extract_raw_sql_queries(path)
    cleaned = normalise_and_filter(raw)
    return tallied_queries(cleaned)
  

if __name__ == "__main__":
  print(build_query_stats(os.getenv("JSONL_FILE_PATH")))


  