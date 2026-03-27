# purpose: extract clean queries from json file
# references: 
# https://www.geeksforgeeks.org/python/read-json-file-using-python

import json;

# replicate something like this inside function, but make sure we only extract sql queries not anything else.
# json_file = "C:\Users\ashut\Desktop\shquery\shquery-sample-mock\logs\queries.json.json"
# try:
#   with open(json_file,'r') as sql_queries_file:
#     captured_queries = json.load(sql_queries_file)
# except FileNotFoundError:
#   raise FileNotFoundError(f"{json_file} not found!")
# except json.JSONDecodeError:
#   raise json.JSONDecodeError(f"JSON @ {json_file} malformed, or incorrectly formatted!")
    
# print(json.dumps(captured_queries, indent=4))


def extract_sql_queries(json_lines_file_path:str):
  """
  Extract SQL queries from JSONL (`JSON-Lines <https://jsonltools.com/what-is-jsonl>`_) log file.

  Args:
    json_lines_file_path (string): Path to the JSONL log file.
    
  Returns:
        List[dict]: A list of dictionaries, each containing:
            - 'sql' (str): The extracted SQL query
            - 'timestamp' (str | None): Timestamp from the log entry
            - 'pid' (int | None): Process ID from the log entry
  """
  