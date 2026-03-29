# purpose: extract clean queries from json file
# references: 
# https://www.geeksforgeeks.org/python/read-json-file-using-python

import json;

def extract_sql_queries(json_lines_file_path:str)->dict:
  """
  Extract SQL queries from JSONL ( `JSON-Lines <https://jsonltools.com/what-is-jsonl>`_) log file.

  Args:
    json_lines_file_path (string): Path to the JSONL log file.
    
  Returns:
        List[dict]: A list of dictionaries, each containing:
            - 'sql' (str): The extracted SQL query
  """
  
  try:
    with open(json_lines_file_path,'r') as log_file:
      # filter to catch sql queries only...
      # reading log line by line, adding it to a dict w/ deduplication/normalisation. T:O(N) S:O(N)
      
      
      pass
  except FileNotFoundError:
    raise FileNotFoundError(f"{json_lines_file_path} not found!")
  