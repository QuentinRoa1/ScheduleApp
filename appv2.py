import sqlite3
from datetime import date
import argparse
from collections import OrderedDict
from operator import itemgetter

class Formaters():
    def print_list(list):
        if not list:
            print("List cannot be shown.") 
            exit
        for row in list:
            line=''
            for item in row:
                if not item==row[-1]:
                    line=line+str(item)+' | '
                else:line = line+str(item)
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
        if data[1]=='today': data[1]=date.today()
        data[2]=Formaters.format_time(str(data[2]))
        data[3]=Formaters.format_time(data[3])
        data.pop(0)
        self.cur.execute('INSERT INTO DATA(date,timefrom,timeto,task,tag) VALUES(date(?),?,?,?,?)',tuple(data))
        self.con.commit()
        print("Data entered")
    def query_table(self,data):
        sql = 'SELECT * FROM DATA WHERE date==date(?) OR task==? OR tag==?'
        if data[1]=='today': self.cur.execute('SELECT * FROM DATA WHERE date==?', (date.today(),))
        else:
            self.cur.execute(sql,(data[1],data[1],data[1]))
        result=self.cur.fetchall()
        if result:
            print("Query results: ")
        else:
            print("None matching your query, here is the full list: ")
            self.cur.execute('SELECT * FROM DATA')
            result= self.cur.fetchall()
        return result
    def get_table(self):
        return self.cur.execute('SELECT * FROM DATA')
    def get_range(self,data):
        data.pop(0)
        if len(data)>2:
            print('To many variables')
            return []
        dates= []
        for date in data:
            if date == 'today':dates.append(date.today())
            else: dates.append(date)
        self.cur.execute('SELECT * FROM DATA WHERE date BETWEEN date(?) AND date(?)',tuple(dates))
        print('record from '+str(dates[0])+' to '+str(dates[1]))
        return self.cur.fetchall()
    def get_highest(self):
        self.cur.execute('SELECT DISTINCT task FROM DATA')
        tasks = self.cur.fetchall()
        if not tasks:
            return []  
        tasksHours = self.calculate_hours(tasks)
        hoursdict = {tasks[i]: tasksHours[i] for i in range(len(tasks))}
        hoursdict = OrderedDict(sorted(hoursdict.items(),key=itemgetter(1)))
        returnlist=[]
        for i in range(3):
            returnlist.append([list(list(hoursdict)[len(hoursdict)-i-1])[0],hoursdict[list(hoursdict)[len(hoursdict)-i-1]]])
        print("Here is what you do the most and how many hours you spent doing it: ")
        return returnlist

    def calculate_hours(self,tasks):
        tasksHours = []
        for task in tasks:
            self.cur.execute('SELECT timefrom FROM DATA WHERE task == ?',task)
            timefrom = list(self.cur.fetchall())
            self.cur.execute('SELECT timeto FROM DATA WHERE task == ?',task)
            timeto = list(self.cur.fetchall())
            hours = 0
            for i in range(len(timefrom)):
                timefrom[i]=str(timefrom[i][0])
                timeto[i]=str(timeto[i][0])
                fromsplit = timefrom[i].split(':')
                tosplit = str(timeto[i]).split(':')
                hours += float(tosplit[0])-float(fromsplit[0])
                minutes = float(tosplit[1])-float(fromsplit[1])
                if minutes>=0:
                    hours += minutes/60
                    continue
                minutes+=60
                hours=hours-1+minutes/60
            tasksHours.append(hours)
        return tasksHours

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
        elif(arg.input[0]== 'report'):
            Formaters.print_list(operations.get_range(arg.input))
        elif(arg.input[0]=='priority'):
            Formaters.print_list(operations.get_highest())
        else: 
            print("Sorry, that command does not exist. We currently support query and insert. Here are your tasks: ")
            Formaters.print_list(operations.get_table())
    else:
        print("Your tasks: ")
        Formaters.print_list(operations.get_table())
main()