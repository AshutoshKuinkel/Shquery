# purpose: extract clean queries from json file
# references: 
# https://www.geeksforgeeks.org/python/read-json-file-using-python

import json;

def extract_sql_queries(json_lines_file_path:str):
  """
  Extract SQL queries from JSONL ( `JSON-Lines <https://jsonltools.com/what-is-jsonl>`_) log file.

  Args:
    json_lines_file_path (string): Path to the JSONL log file.
    
  Returns:
        List[dict]: A list of dictionaries, each containing:
            - 'sql' (str): The extracted SQL query
            - 'timestamp' (str | None): Timestamp from the log entry
            - 'pid' (int | None): Process ID from the log entry
  """
  try:
    with open(json_lines_file_path,'r') as log_file:
      # filter to catch sql queries only...
      # we could read the whole file and scan for certain keywords to filter for sql queries only
      # but is there a more efficient way of filtering out only SQL queries?? ahh I don't think so,
      # either way O(N) time complexity will be required...
      pass
  except FileNotFoundError:
    raise FileNotFoundError(f"{json_lines_file_path} not found!")
  