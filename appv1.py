import sqlite3
from datetime import date
import argparse
def get_date():
  return(date.today())
class Formaters():
    def print_list(list=["Nothing here"]):
        for row in list:
            line=''
            for item in row:
                if not item==row[-1]:
                    line=line+str(item)+' | '
                line = line+str(item)
            print(line)
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
class Operations():
    def __init__(self):
        self.con = sqlite3.connect('library.db') 
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS DATA (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, date DATE,timefrom TEXT ,timeto TEXT, task TEXT, tag TEXT);')
    def add_row(self,data):
        if data[1]=='today': data[1]=get_date()
        data[2]=Formaters.format_time(str(data[2]))
        data[3]=Formaters.format_time(data[3])
        data.pop(0)
        self.cur.execute('INSERT INTO DATA(date,timefrom,timeto,task,tag) VALUES(?,?,?,?,?)',tuple(data))
        self.con.commit()
        print("Data entered")
    def query_table(self,data):
        sql = 'SELECT * FROM DATA WHERE date==? OR task==? OR tag==?'
        if data[1]=='today': self.cur.execute('SELECT * FROM DATA WHERE date==?', (get_date(),))
        else:
            self.cur.execute(sql,(data[1],data[1],data[1]))
        result=self.cur.fetchall()
        if result:
            print("Query results: ")
            
        else:
            print("None matching your query, here is the full list: ")
            self.cur.execute('SELECT * FROM DATA')
            result=self.cur.fetchall()
        return result
    def get_table(self):
        return self.cur.execute('SELECT * FROM DATA')
def main():
    operations=Operations()
    parser=argparse.ArgumentParser()
    parser.add_argument('input', nargs='*' )
    arg=parser.parse_args()
    if arg.input:
        if (arg.input[0]=='query'):
            Formaters.print_list(operations.query_table(arg.input))
        elif(arg.input[0]== 'record'):
            operations.add_row(arg.input)
        else: 
            print("Sorry, that command does not exist. We currently support query and insert. Here are your tasks: ")
            Formaters.print_list(operations.get_table())
    else:
        print("Your tasks: ")
        Formaters.print_list(operations.get_table())
main()