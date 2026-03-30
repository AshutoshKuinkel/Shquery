# purpose: extract clean queries from json file
# references: 
# https://www.geeksforgeeks.org/python/read-json-file-using-python
# https://www.geeksforgeeks.org/python/json-loads-in-python
# DDL VS DML: https://www.geeksforgeeks.org/dbms/difference-between-ddl-and-dml-in-dbms

import json;

def extract_sql_queries(json_lines_file_path:str)->dict:
  """
  Extract SQL queries from JSONL ( `JSON-Lines <https://jsonltools.com/what-is-jsonl>`_) log file.

  Args:
    json_lines_file_path (string): Path to the JSONL log file.
    
  Returns:
        dict: A list of dictionaries, each containing:
            - 'sql' (str): The extracted SQL query
  """
  # approach:
  # filter to catch sql queries only...
  # reading log line by line, adding it to a dict w/ deduplication/normalisation. T:O(N) S:O(N)
  # normalisation with pg_query... & then run EXPLAIN for costs plan... 
  clean_queries = {}
  try:
    with open(json_lines_file_path,'r') as file:
      for line in file:
        line.strip()
        
        try:
          py_obj_query = json.loads(line)
        except json.JSONDecodeError:
          # more suitable to throw continue here instead of JSONDecodeErr, so whole pipeline doesn't break.
          continue
        
        dml_query = py_obj_query.get('message','')
        if dml_query.startsWith('execute'):
          # TO DO: strip the exectue queries, those are what we need... then just add normalisation/deduplication
          pass
        
      
      
      
  except FileNotFoundError:
    raise FileNotFoundError(f"{json_lines_file_path} not found!")
  