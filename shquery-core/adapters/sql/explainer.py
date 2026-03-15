# When running EXPLAIN in Postgres, it returns plain text rows e.g.:
# Seq Scan on users  (cost=0.00..18334.00 rows=1000000 width=68)
# Thats just string. There's no structured JSON or object, only raw text. So explainer is just extracting useful numbers and words out of that string.