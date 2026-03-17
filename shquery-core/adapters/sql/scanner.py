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
# On discussion with people, I may have to use a custom annotation/interface for 100% coverage and to 
# make it easier to detect sql queries... This'll work well for raw sql, but I still need to think about
# jpql etc..
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
      
      if file.endsWith(".java"):
        java_files.append(path)
        
      if file.endsWith(".js"):
        javascript_files.append(path)
        
      if file.endsWith(".ts"):
        typescript_files.append(path)
  
  
