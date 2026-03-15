from pathlib import Path;
from sqlglot import parse_one,exp;
import sqlglot;

# grab source code
source_code = Path("shquery-sample-mock/users/mock-users.sql").read_text()

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

statements = sqlglot.parse(source_code, dialect="postgres")

for statement in statements:
  if statement:
    print(extract_features(statement))
    print("----")