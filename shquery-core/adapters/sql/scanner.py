# Current task:
# Repo Scanner
#     │
#     ▼
#File Discovery
#     │
#     ▼
#Language Detection
#     │
#     ▼
#AST Parser (per language) {call this only after we've filtered out files that don't contain any db related code}
#     │
#     ▼
#Rule Engine
#     │
#     ▼
#SQL Extraction
# To improve performance, just make sure we skip venv, node_modules and all that stuff
# Also use like a keyword prefilter saying like if SELECT or whatever dml not in file, skip file
import os;

def scan_codebase(directory):
  sql_files=[] #to handle all .sql files 
  migration_scripts=[] #to handle all *.migration.* files
  java_files=[] # to handle JPA Entity
  javascript_files=[]
  typescript_files=[]
  
  
  
  for root,dirs, files in os.walk(directory):
    for file in files:
      path = os.path.join(root,file)
      
      # sql files
      if file.endsWith("sql"):
        sql_files.append(path)
  
  
