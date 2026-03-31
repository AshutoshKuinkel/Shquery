# purpose: extract clean queries from json file
# references: 
# https://www.geeksforgeeks.org/python/read-json-file-using-python
# https://www.geeksforgeeks.org/python/json-loads-in-python
# DDL VS DML: https://www.geeksforgeeks.org/dbms/difference-between-ddl-and-dml-in-dbms

import json;
import os
from dotenv import load_dotenv
load_dotenv()


def extract_sql_queries(json_lines_file_path:str)->list:
  """
  Extract SQL queries from JSONL ( `JSON-Lines <https://jsonltools.com/what-is-jsonl>`_) log file.

  Args:
    json_lines_file_path (string): (Path to the JSONL log file.)
    
  Returns:
        dict: A list of dictionaries, each containing:
            - 'sql' (str): The extracted SQL query
  """
  # approach:
  # filter to catch sql queries only...
  # reading log line by line, adding it to a dict w/ deduplication/normalisation. T:O(N) S:O(N)
  # normalisation with pg_query... & then run EXPLAIN for costs plan... 
  
  # this is only a list for testing purposes, but lookups in list take O(N) and in dicts take O(1) time, so change to dict for performance..
  clean_queries = []
  try:
    with open(json_lines_file_path,'r') as file:
      for line in file:
        line = line.strip()
        
        try:
          py_obj_query = json.loads(line)
        except json.JSONDecodeError:
          # more suitable to throw continue here instead of JSONDecodeErr, so whole pipeline doesn't break.
          continue  
        
        dml_query = py_obj_query.get('message','')
        if dml_query.startswith('execute'):
          # TO DO: handle \n cases... then just add normalisation/deduplication
          sql = dml_query.split(":",1)[1].strip()
          clean_queries.append(sql)
        else:
          continue
        
    return clean_queries;  
      
  except FileNotFoundError:
    raise FileNotFoundError(f"{json_lines_file_path} not found!")
  
  
if __name__ == "__main__":
  print(extract_sql_queries(os.getenv('JSONL_FILE_PATH')))
  