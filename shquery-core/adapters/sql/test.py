from pathlib import Path;
from sqlglot import parse_one,exp;
import sqlglot;
import psycopg2;
import os;
from dotenv import load_dotenv;


load_dotenv()

# grab source code
source_code = Path("shquery-sample-mock/users/mock-users.sql").read_text()

conn = psycopg2.connect(
  dbname=os.getenv("DB_NAME"),
  user=os.getenv("DB_USER"),
  password=os.getenv("DB_PASSWORD"),
  host=os.getenv("DB_HOST"),
  port=5432
)
print(conn)
# # call sqlglot to handle this:
# def parse_query(code):
#   try:
#     # convert into the tree structure w nodes representing valid language constructs:
#     return sqlglot.parse_one(code,dialect="postgres")
#   except sqlglot.errors.ParseError:
#     return None
  
# go through and extract some key features from AST:
def extract_features(ast):
  tables = [t.name for t in ast.find_all(exp.Table) if t.name]
  
  where_node = ast.find(exp.Where)
  where_conditions = len(list(ast.find_all(exp.Condition))) if where_node else 0
  return{
    "statement_type": type(ast).__name__,
    
    "tables" : list(set(tables)),
    "table_count" : len(set(tables)),
    
    "join_count" : len(list(ast.find_all(exp.Join))),
    "join_types" : [j.side or "CROSS" for j in ast.find_all(exp.Join)],
    
    "has_where" : where_node is not None,
    "where_conditions" : where_conditions,
    "has_like" : ast.find(exp.Like) is not None,
    
    "has_group_by" : ast.find(exp.Group) is not None,
    "has_having" : ast.find(exp.Having) is not None,
    "aggregations" : [a.sql() for a in ast.find_all(exp.AggFunc)],
    
    "is_select_star" : ast.find(exp.Star) is not None,
    "column_count" : len(list(ast.find_all(exp.Column))),
    
    "subquery_count" : len(list(ast.find_all(exp.Subquery))),
    
    "has_order_by" : ast.find(exp.Order) is not None,
    "has_limit" : ast.find(exp.Limit) is not None,
  
    "is_write_operation" : bool(ast.find(exp.Insert) or ast.find(exp.Update) or ast.find(exp.Delete))
  }


def prase_explain(explain_rows):
  raw = "\n".join(row[0] for row in explain_rows)
    
  import re
  cost_match = re.search(r'cost=(\d+\.\d+)\.\.(\d+\.\d+)', raw)
  rows_match = re.search(r'rows=(\d+)', raw)
    
  scan_type = "Unknown"
  if "Bitmap Heap Scan" in raw:
    scan_type = "Bitmap Heap Scan"
  elif "Index Only Scan" in raw:
    scan_type = "Index Only Scan"
  elif "Index Scan" in raw:
    scan_type = "Index Scan"
  elif "Seq Scan" in raw:
    scan_type = "Seq Scan"
        
  return {
      "scan_type": scan_type,
      "cost_start": float(cost_match.group(1)) if cost_match else None,
      "cost_total": float(cost_match.group(2)) if cost_match else None,
      "estimated_rows": int(rows_match.group(1)) if rows_match else None,
      "raw_plan": raw
  }
    
statements = sqlglot.parse(source_code, dialect="postgres")
ddl_types={"Create","Drop","Insert","Alter","Truncate"}

# DDL schemas first then only run explain,
# else we'll get err when running EXPLAIN and
# we don't have any tables or anything.
with conn.cursor() as cur:
  for statement in statements:
    if statement and type(statement).__name__ in ddl_types:
      try:
        cur.execute(statement.sql(dialect="postgres"))
        conn.commit()
      except Exception as e:
        print(f"DDL Err: {e}")
        conn.rollback()
        
  for statement in statements:
    if statement and type(statement).__name__ == "Select":
      features = extract_features(statement)
      
      try:
        cur.execute(f"EXPLAIN {statement.sql(dialect='postgres')}")
        explain_output = prase_explain(cur.fetchall())
        
        print("features:",features)
        print("EXPLAIN:", explain_output)
        print("---")
      except Exception as e:
        print(f"EXPLAIN ERROR: {e}")
        