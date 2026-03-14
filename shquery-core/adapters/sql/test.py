from pathlib import Path;
from sqlglot import parse_one;
import sqlglot;

# grab source code
source_code = Path("shquery-sample-mock/users/mock-users.sql").read_text()

# call sqlglot to handle this:
def parse_query(source_code):
  try:
    # convert into the tree structure w nodes representing valid language constructs:
    return sqlglot.parse_one(source_code,dialect="postgres")
  except sqlglot.errors.ParseError:
    return None

ast = parse_query(source_code)
print(repr(ast))