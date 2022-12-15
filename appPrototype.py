import sqlite3
from datetime import date
import argparse

con = sqlite3.connect('library.db') 
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS DATA (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date DATE,timefrom TEXT ,timeto TEXT, task TEXT, tag TEXT);')
def print_list(list=["Nothing here"]):
  for row in list:
    print(row)
def get_date():
  return(date.today())
def format_time(time):
  if 'AM' in time or 'am' in time:
    return time.replace('am','').replace('AM','')
  if 'PM' in time or 'pm' in time:
    time = time.replace('pm','').replace('PM','')
    li = list(time)
    if len(li)<5:
      li.insert(0,'1')
    else: li[0]= str(int(li[0])+1)
    li[1]= str(int(li[1])+2)
    return ''.join(li)
  return time


def add_row(data):
  if data[1]=='today': data[1]=get_date()
  data[2]=format_time(data[2])
  data[3]=format_time(data[3])
  data.pop(0)
  cur.execute('INSERT INTO DATA(date,timefrom,timeto,task,tag) VALUES(?,?,?,?,?)',tuple(data))
  con.commit()
  print("Data entered")
def query_table(data):
  sql = 'SELECT * FROM DATA WHERE date==? OR task==? OR tag==?'
  if data[1]=='today': cur.execute('SELECT * FROM DATA WHERE date==?', (get_date(),))
  else:
    cur.execute(sql,(data[1],data[1],data[1]))
  result=cur.fetchall()
  if result:
    print("Query results: ")
    return result
  else:
    print("None matching your query, here is the full list: ")
    cur.execute('SELECT * FROM DATA')
    return cur.fetchall()
def get_table():
  return cur.execute('SELECT * FROM DATA')
parser=argparse.ArgumentParser()
parser.add_argument('input', nargs='*' )
arg=parser.parse_args()
if arg.input:
  if (arg.input[0]=='query'):
    print_list(query_table(arg.input))
  elif(arg.input[0]== 'record'):
    add_row(arg.input)
  else: 
    print("Sorry, that command does not exist. We currently support query and insert. Here are your tasks: ")
    print_list(get_table())
else:
  print("Your tasks: ")
  print_list(get_table())