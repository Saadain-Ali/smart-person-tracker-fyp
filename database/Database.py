import sqlite3
from datetime import datetime
from sqlite3.dbapi2 import DatabaseError
# from static.variables import *
# import time
# import datetime
# import random

# # conn = sqlite3.connect('Proj.db')
# conn = None
# c = None

# def create_table():
#     # c.execute("""CREATE TABLE students(
#     #     sid text,
#     #     name text,
#     #     email text)""")
#     c.execute('''CREATE TABLE "student_info" (
# 	    "StudentId"	INTEGER NOT NULL,
# 	    "Location"	TEXT NOT NULL,
# 	    "TimeStamp"	TEXT NOT NULL,
# 	    FOREIGN KEY("StudentId") REFERENCES students("rowid"))''')


# def add_student(name , sid , email):
#     with conn:
#         c.execute("INSERT INTO students VALUES (?,?,?)",(sid,name,email))

# def search_all():
#     with conn:
#         c.execute("SELECT * FROM students ")
#         data = c.fetchall()
#         for row in data:
#             print(row)

# def add_students(students_list):
#     conn = sqlite3.connect('Proj.db')
#     c = conn.cursor()
#     # c.execute("INSERT INTO stuffToPlot VALUES(1452549219,'2016-01-11 13:53:39','Python',6)")
#     c.execute("INSERT INTO customers VALUES (?,?,?)",(students_list))
#     conn.commit()


# def read_student_from_db():
#     conn = sqlite3.connect('Proj.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM students')
#     data = c.fetchall()
#     print(data)
#     for row in data:
#         print(row)

# def search_student_id(id):
#     conn = sqlite3.connect('Proj.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM students WHERE sid = (?)',(id,))
#     data = c.fetchall()
#     for row in data:
#         print(row)

# def search_student_name(name):
#     conn = sqlite3.connect('Proj.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM students WHERE name = (?)',(name,))
#     data = c.fetchall()
#     for row in data:
#         print(row)

# def search_student_email(email):
#     conn = sqlite3.connect('Proj.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM students WHERE email = (?)',(email,))
#     data = c.fetchall()
#     for row in data:
#         print(row)



# # create_table()
# # search_student_email("ali.saadain@gmail.com")
# # c.close
# # conn.close()


class info_extractor:
    # params = first_name,last_name,sid,email
    def student_countByName(name):
        """
        query student by given parameters
        """
        conn = sqlite3.connect('database/student.db')
        # print("Opened database successfully")
        _query = f"""
        SELECT f.student_1 as sid , s.first_name as name, COUNT(f.student_1) AS cnt
        FROM finds as f
        JOIN student as s
        ON s.sid = f.student_1
        WHERE s.first_name = "{name}"
        """
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchone()  #returns a (tuple)
            row = list(row)
        except DatabaseError as identifier:
            print(identifier)
            row = []
        finally:
            conn.close() 
            return row
        # rows = cursor.fetchall()  #returns list[(tuple)]
        # print(type(rows))
        # for row in rows:
        #     print("sid \t name \t occurence")
        #     print(str(row[0]) +' \t' +  row[1] +' \t ' + str(row[2]))
        #     print()
        # conn.close() 
    
    def student_countByID(sid):
        """
        query student by given parameters
        """
        conn = sqlite3.connect('database/student.db')
        # print("Opened database successfully")
        _query = f"""
        SELECT f.student_1 as sid , s.first_name as name, COUNT(f.student_1) AS cnt
        FROM finds as f
        JOIN student as s
        ON s.sid = f.student_1
        WHERE s.sid = '{sid}';
        """
        rows = []
        try:
            cursor = conn.execute(_query)
            # row = cursor.fetchone()  #returns a (tuple)
            rows = cursor.fetchall()  #returns list[(tuple)]
            print(type(rows))
            for row in rows:
                print("sid \t name \t occurence")
                print(str(row[0]) +' \t' +  row[1] +' \t ' + str(row[2]))
                print()
        except DatabaseError as identifier:
            print(identifier)
            rows = []
        finally:
            conn.close()
            return rows
        

    def student_maxOccur(sid):
        """
        query the max occurence of student in given location
        """
        conn = sqlite3.connect('database/student.db')
        # print("Opened database successfully")
        _query = f"""
        SELECT s.first_name as name,f.location,f.date ,COUNT(f.student_1) AS cnt,sum(f.time) as Ttime
        FROM finds as f
        JOIN student as s
        ON s.sid = f.student_1
        WHERE  f.student_1 = '{sid}' 
        GROUP BY f.student_1,f.location,f.date
        ORDER BY cnt DESC;
        """
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchall()  #returns a (tuple)
            row = list(row)
        except DatabaseError as identifier:
            print(identifier)
            row = []
        finally:
            conn.close() 
            return row
    
    def find_lastSeen(sid,date):
        """
        #is me date bhi daalo
        No of Occurence in specific places
        """
        curr_date = date
        conn = sqlite3.connect('database/student.db')
        # print("Opened database successfully")
        _query = f"""
        SELECT s.first_name, f.student_1 , s2.first_name as name2  , f.student_2 as sid2, f.time , f.location
            FROM student as s, student as s2
            join finds as f 
            on s.sid = f.student_1 and (f.student_2 = s2.sid or f.student_2 is null)
            where f.date = '{curr_date}' and  s.sid = {sid}
            GROUP BY f.student_1 ,f.student_2
            ORDER BY f.time DESC;
        """
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchone()  #returns a (tuple)
            row = list(row)
        except DatabaseError as identifier:
            print(identifier)
            row = []
        finally:
            conn.close() 
            return row
    
    def student_withStudentEveryOccur(sid1,sid2):
        """
        No of occurence of two students
        """
        conn = sqlite3.connect('database/student.db')
        # print("Opened database successfully")
        _query = f"""
        SELECT f.student_1 as student1 , f.student_2 as student2 , f.location as location, COUNT(f.student_1) AS cnt
        FROM finds as f
        JOIN student as s
        ON s.sid = f.student_1
        where f.student_1 = {sid1} and f.student_2 = {sid2}
        """
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchone()  #returns a (tuple)
            row = list(row)
            conn.close() 
        except DatabaseError as identifier:
            print(identifier)
        finally:
            return row

    def student_All():
        """
        Return All students
        """
        with sqlite3.connect('database/student.db') as conn:
            # print("Opened database successfully")
            _query = f"""
            SELECT * FROM student
            """
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchall()  #returns a (tuple)
            row = list(row)
        except DatabaseError as identifier:
            print(identifier)
            row = []
        finally:
            conn.close() 
            return row

    # findAllFreinds(sid)
    def findAllFreinds(sid,current_date):
        with sqlite3.connect('database/student.db') as conn:
            print(f'{current_date}  {sid}')
            _query = f"""
               SELECT s.first_name, finds.date ,f2.time as arriving_time, f2.location as first_detect, finds.time as leaving_time, finds.location as last_detect
                FROM finds, finds f2,student s
                WHERE (finds.student_1 = '{sid}' and s.sid = '{sid}' and f2.student_1 = '{sid}' ) AND (finds.date = '{current_date}' AND f2.date = '{current_date}')
                ORDER BY finds.time DESC
                LIMIT 1
                """
            row = []
            try:
                cursor = conn.execute(_query)
                row = cursor.fetchall()  #returns a (tuple)
                print(row)
            except DatabaseError as identifier:
                print("error " + str(identifier))
            finally:
                return row
    
        # findAllFreinds(sid)
    
    def findStudentFreinds(sid):
        with sqlite3.connect('database/student.db') as conn:
            _query = f"""
                SELECT f.student_1 as student1 , f.student_2 as student2 , f.location as location, COUNT(f.student_1) AS cnt
                    FROM finds as f
                    JOIN student as s
                    ON s.sid = f.student_1
                    where f.student_1 = 62647
                    GROUP BY f.student_2
                    ORDER BY cnt DESC; 
                """
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchall()  #returns a (tuple)
            row = list(row)
        except DatabaseError as identifier:
            print(identifier)
            row = []
        finally:
            conn.close() 
            return row

    def findRoute(sid,date):
        with sqlite3.connect('database/student.db') as conn:
            _query = f'''
            SELECT DISTINCT s.first_name ,finds.student_1,finds.date, finds.location as arriving, finds.time as arriving_time 
            FROM finds, finds f2
            JOIN student s
            on s.sid = finds.student_1
            WHERE (finds.student_1 = {sid} AND finds.date = '{date}') AND (f2.student_1 = {sid} AND f2.date = '{date}')
            GROUP BY finds.location
            ORDER BY f2.time DESC, arriving_time;
            '''
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchall()  #returns a (tuple)
            row = list(row)
        except DatabaseError as identifier:
            print(identifier)
            row = []
        finally:
            conn.close() 
            return row

    # Find Where with Friend
    def findFriendOccur(sid1,sid2):
        with sqlite3.connect('database/student.db') as conn:
           _query = f'''
            SELECT s.first_name as s_1, s2.first_name as s_2, f.location as location, COUNT(f.student_1) AS cnt
                FROM student as s, student as s2
                JOIN finds as f
                ON s.sid = f.student_1 and s2.sid = f.student_2
                where f.student_1 = {sid1} and f.student_2 = {sid2}
				GROUP BY f.location;
           '''
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchall()  #returns a (tuple)
            row = list(row)
        except DatabaseError as identifier:
            print(identifier)
            row = []
        finally:
            conn.close() 
            return row
    
    # Clocked in and out 
    def findClockedInOut(sid , current_date):
        row = []
        with sqlite3.connect('database/student.db') as conn:
           _query = f'''
            SELECT finds.student_1, finds.date ,f2.time as arriving_time, f2.location as first_detect, finds.time as leaving_time, finds.location as last_detect
                FROM finds, finds f2
                WHERE (finds.student_1 = {sid} and f2.student_1 = {sid}) AND (finds.date = '{current_date}' AND f2.date = '{current_date}')
                ORDER BY finds.time DESC
                LIMIT 1
           '''
           
           try:
               cursor = conn.execute(_query)
               row = cursor.fetchone()  #returns a (tuple)
               row =  list(row)
           except EnvironmentError as identifier:
               row = []
           finally:
               return row

    def findAllatOnePlace(location):
        with sqlite3.connect('database/student.db') as conn:
            _query = f"""
                SELECT DISTINCT  s1.first_name as s_1 , finds.student_1 , s2.first_name as s_2, finds.student_2 ,COUNT(finds.student_1) as cnt
                    FROM finds,student as s1 , student as s2
                    WHERE location = '{location}' AND s1.sid = finds.student_1 AND s2.sid = finds.student_2
                    GROUP BY finds.student_1 , finds.student_2
                    ORDER BY finds.student_1,cnt DESC; 
                """
            cursor = conn.execute(_query)
            row = cursor.fetchall()  #returns a (tuple)
            print(row)
            return list(row)

        # make it a seperate thread
    
    def getData(sid):
        row = []
        conn = sqlite3.connect('database/student.db')
        # print("Opened database successfully")
        cursor = conn.execute("SELECT first_name,last_name,sid,email,age,gender From student WHERE first_name = " + '"' + sid + '"')
        # for row in cursor:
        #     print("first_name " + row[0])
        #     print("last_name " + row[1])
        #     print("sid " + row[2])
        #     print("email " + row[3])
        #     print("age  " + row[4])
        #     print("gender  " + row[5])
        # print("Operation done successfully")
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

    def getFindsData():
        """
        Return All finds
        """
        with sqlite3.connect('database/student.db') as conn:
            # print("Opened database successfully")
            _query = f"""
            SELECT * FROM finds
            """
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchall()  #returns a (tuple)
            row = list(row)
        except DatabaseError as identifier:
            print(identifier)
            row = []
        finally:
            conn.close() 
            return row
    

# ============== FOR DASHBOARD ==============
    def getTotalOccurences():
        '''
        Returns total occurences overall data
        '''
        with sqlite3.connect('database/student.db') as conn:
            # print("Opened database successfully")
            _query = f"""
            SELECT count(student_1) from finds;  
            """
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchone() 
        except DatabaseError as identifier:
            print(identifier)
            row = 0
        finally:
            conn.close() 
            return row

    def getTotalOccurencesToday():
        '''
        Returns total occurences TODAY
        '''
        
        with sqlite3.connect('database/student.db') as conn:
            # print("Opened database successfully")
            _query = f"""
            SELECT count(finds.student_1) from finds where finds.date = '{datetime.now().strftime('%d-%m-%Y')}';
            """
        print(_query)
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchone() 
        except DatabaseError as identifier:
            print(identifier)
            row = 0
        finally:
            conn.close() 
            return row

    def getDashboardData():
        '''
        Returns dashboards data
        '''
        with sqlite3.connect('database/student.db') as conn:
            # print("Opened database successfully")
            _query = f"""
            SELECT (count(sid)-1) from student; 
            """
        row = {
            'students' : 0,
            'occurencesToday' : 0,
            'occurences' : 0
        }
        try:
            cursor = conn.execute(_query)
            row['students'] = cursor.fetchone()[0] 
        except DatabaseError as identifier:
            print(identifier)
            row = 0
        finally:
            conn.close() 
            return row
# ============== DASHBOARD ENDS ==============

# ===================== CHARTS DATA =====================
    def getMostVisitedLocation():
        '''
        Returns 
        '''
        with sqlite3.connect('database/student.db') as conn:
            # print("Opened database successfully")
            _query = f"""
             SELECT f.location , count(f.location) as count from finds f GROUP by f.location 
            """
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchall() 
            # print(row)
        except DatabaseError as identifier:
            print(identifier)
            row = 0
        finally:
            conn.close() 
            return row

    def getHeatMapofOccurences(sid = None):
        '''
        Returns heatmap by date 
        '''

        with sqlite3.connect('database/student.db') as conn:
            if sid == None:
                print('sid = None')
                # print("Opened database successfully")
                _query = f"""
                SELECT f.date , count(f.date) as count from finds f GROUP by f.date
                """
            else:
                _query = f"""
                SELECT f.date , count(f.date) as count from finds f where f.student_1 == '{sid}' GROUP by f.date
                """
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchall() 
            # print(row)
        except DatabaseError as identifier:
            print(identifier)
            row = 0
        finally:
            conn.close() 
            return row


    def getTimeLineByLocation(_date , sid):
        '''
        Returns heatmap by date 
        '''
        with sqlite3.connect('database/student.db') as conn:
            # print("Opened database successfully")
            _query = f"""
                SELECT f.date, min(f.time) as first, max(f.time) as last , f.location 
                from finds f 
                where 
                f.date = '{_date}' and f.student_1 = '{sid}'
                GROUP by f.location            
             """
            print(_query)
        row = []
        try:
            cursor = conn.execute(_query)
            row = cursor.fetchall() 
            print(row)
        except DatabaseError as identifier:
            print(identifier)
            row = 0
        finally:
            conn.close() 
            return row

# ===================== CHARTS DATA END=====================