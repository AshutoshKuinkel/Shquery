# purpose: extract clean queries from json file
# references: 
# https://www.geeksforgeeks.org/python/read-json-file-using-python
# https://www.geeksforgeeks.org/python/json-loads-in-python
# DDL VS DML: https://www.geeksforgeeks.org/dbms/difference-between-ddl-and-dml-in-dbms
# MD5: https://www.geeksforgeeks.org/python/md5-hash-python/

import json;
import os
import hashlib;
from dotenv import load_dotenv
load_dotenv()

#  the key worry is more so, how do I determine what makes 2 queries the same for deduplication...

# approach:
# filter to catch sql queries only...
# reading log line by line, adding it to a dict w/ deduplication/normalisation. T:O(N) S:O(N)
# then run EXPLAIN for costs plan... 
# also add a count frequency after normalisation/deduplication which will help performance analysis, identifying hot queries/deciding what to optimise

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
    
    if sql.split[0] in DDL_WORDS:
      continue
    
    clean_queries.append(sql)
    
    return clean_queries
  
  
  
if __name__ == "__main__":
  print(extract_raw_sql_queries(os.getenv('JSONL_FILE_PATH')))
  


  