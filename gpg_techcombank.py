import os
from dotenv import load_dotenv
import psycopg2
import sys
import re
# import subprocess


class PostgresConnector():
  def __init__(self, db_host, db_name_table, db_port, db_username, db_passwd) -> None:
    self.host = db_host
    self.dbname = db_name_table
    self.port = db_port
    self.user = db_username
    self.passwd = db_passwd
    self.connection_string = f"host={db_host} dbname={db_name_table} user={db_username} password={db_passwd} port={db_port}"
      
  def check_connection(self):
    try:
      conn = psycopg2.connect(self.connection_string)
      cursor = conn.cursor()
      cursor.execute("SELECT 1")
      cursor.close()
      conn.close()
      print(f"Connection to database {self.dbname} in host {self.host} : up")
      return True
    # except RuntimeError as e:
    # except Exception as e:
    except psycopg2.OperationalError as e:
    # except:
      print("Something else went wrong")
      print(e)
      # set exit status when check_connection failed -- echo $?
      sys.exit(9)
      return False
  
  def execute_query(self, query_string, is_many=False, data=[]):
    if self.check_connection:
      client = psycopg2.connect(self.connection_string)
    else:
      sys.exit(0)
      
    conn = client.cursor()
    try:
      if data:
        if is_many:
          conn.executemany(query_string, data)
          # result = conn.fetchall()
        else:
          conn.execute(query_string, data)
          # result = conn.fetchone()
      else:
        conn.execute(query_string)
        # result = conn.fetchone()
      
      # try - except when no result to fetch --> when using insert - delete sql
      try:
        result = conn.fetchall()
        # print(result)
      except Exception as e:
        result = []
        print(e)
        
      client.commit()
      conn.close()
      client.close()
      return result
    # try - except when have issue when "if-else" conditions - conn.exucute run
    except Exception as e:
      print(e)
    
    




if __name__ == "__main__":
  load_dotenv()
  
  DB_HOST = os.environ.get("DB_HOST")
  DB_PORT = os.environ.get("DB_PORT")
  DB_USERNAME = os.environ.get("DB_USERNAME")
  DB_PASSWORD = os.environ.get("DB_PASSWORD")
  DB_DATABASE = os.environ.get("DB_DATABASE")
  TCB_RECEIVED = os.environ.get("TCB_RECEIVED")
  tcb_conn = PostgresConnector(db_host=DB_HOST, db_name_table=DB_DATABASE, db_username=DB_USERNAME, db_passwd=DB_PASSWORD, db_port=DB_PORT)
  
  
  # return all info form db
  # query = "SELECT current_database()"
  query = "SELECT * FROM encrypt"
  # query = "DROP TABLE encrypt"
  if tcb_conn.check_connection():
    result_sql = tcb_conn.execute_query(query_string=query)
  result_sql_tuple = tuple(result_sql)
  
  
  # list all file .zip -- list: file_zip_list -- prepare for logic
  file_zip_list = []
  for x in os.listdir():
    # print(x)
    xx = re.match('^([^.]+.txt)$', x)
    if xx:
      # print(xx.group())
      file_zip_list.append(xx.group())
  # print(file_zip_list)
  
  
  # check gpg installed
  y = os.popen('which gpg')
  if y.read().rstrip('\n').split('\n')[0] == '':
    print('gpg was not installed, please install it')
    sys.exit(90)
  else:
    print('gpg was installed')
  
  # generate a list from tuble result database
  file_db_result = []
  check_var = False
  for x in result_sql_tuple:
    file_db_result.append(x[1])
    
  # logic for encrypting file - using public key from partner
  file_zip_db = []
  for x in file_zip_list:
    if x not in file_db_result:
      print(f'file {x} in not in db')
      try:
        os.popen(f'gpg --output {x}.gpg --encrypt --recipient {TCB_RECEIVED} {x}')
        file_zip_db.append(x)
        check_var = True
      except Exception as e:
        print(e)
        sys.exit(95)
    else:
      print(f'file {x} is in db')

  # insert file_name to db if it do not exists
  if check_var:
    for x in file_zip_db:
      query = "INSERT INTO encrypt (name_file) values (%s)"
      x = tcb_conn.execute_query(query_string=query, is_many=False, data=[x])
  else:
    print('inside else : check_var failed')