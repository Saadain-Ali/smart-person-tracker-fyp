from sqlite3.dbapi2 import DatabaseError
from static.model import student
from database.csv_editor import csv_editor as editor
import sqlite3

class data_handle:


    def __init__(self,student_1,student_2,location,date,time):
        self.student_1 = student_1 
        self.student_2 = student_2 
        self.location  = location  
        self.date      = date 
        self.time      = time
    
    def found(self):
        fieldnames = ['student_1','student_2','location','date','time']
        csv_file = editor('database/finds.csv',fieldnames)
        data = {
            'student_1' : self.student_1,
            'student_2' : self.student_2,
            'location'  : self.location,
            'date'      : self.date,
            'time'      : self.time
         }
        csv_file.append_file(data)

    def store_to_DB(self):
        """
        write code to store data to db on runtime
        """
        name2 = ""
        if len(self.student_2) > 0:
            name2 = self.student_2
        else:
            name2 = 'NULL'
        with sqlite3.connect('database/student.db') as conn:
           _query = f"""
              INSERT INTO finds (student_1,student_2,Location,date,time)
                VALUES({self.student_1},{name2},'{self.location}','{self.date}','{self.time}');
               """
           row = []
           try:
               cursor = conn.execute(_query)
               conn.commit()
               row = cursor.lastrowid()
               print("row is added swith success",end='')
               print(row)
           except DatabaseError as identifier:
               print("error " + str(identifier))
           finally:
               return row
    # make it a seperate thread
    def getData(sid):
        row = []
        conn = sqlite3.connect('database/student.db')
        # print("Opened database successfully")
        cursor = conn.execute("SELECT first_name,last_name,sid,email,age,gender From student WHERE first_name = " + '"' + sid + '"')
        row = cursor.fetchone()
        # print(row)
        conn.close()
        if row:
            return {
                'first_name' :  row[0] ,
                'last_name' :   row[1],
                'sid':  row[2],
                'email' :   row[3],
                'age' :     row[4],
                'gender' :  row[5]
            }
        return None
