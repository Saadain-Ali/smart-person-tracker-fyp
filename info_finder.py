import sqlite3

class info_extractor:
    # params = first_name,last_name,sid,email
    def student_countByID():
        """
        query student by given parameters
        """
        conn = sqlite3.connect('student.db')
        # print("Opened database successfully")
        _query = """
        SELECT f.student_1 as sid , s.first_name as name, COUNT(f.student_1) AS cnt
        FROM finds as f
        JOIN student as s
        ON s.sid = f.student_1
        GROUP BY f.student_1
        ORDER BY cnt DESC;
        """
        cursor = conn.execute(_query)
        # row = cursor.fetchone()  #returns a (tuple)
        rows = cursor.fetchall()  #returns list[(tuple)]
        print(type(rows))
        for row in rows:
            print("sid \t name \t occurence")
            print(str(row[0]) +' \t' +  row[1] +' \t ' + str(row[2]))
            print()
        conn.close() 
    
    def student_countByID():
        """
        query student by given parameters
        """
        conn = sqlite3.connect('student.db')
        # print("Opened database successfully")
        _query = """
        SELECT f.student_1 as sid , s.first_name as name, COUNT(f.student_1) AS cnt
        FROM finds as f
        JOIN student as s
        ON s.sid = f.student_1
        GROUP BY f.student_1
        ORDER BY cnt DESC;
        """
        cursor = conn.execute(_query)
        # row = cursor.fetchone()  #returns a (tuple)
        rows = cursor.fetchall()  #returns list[(tuple)]
        print(type(rows))
        for row in rows:
            print("sid \t name \t occurence")
            print(str(row[0]) +' \t' +  row[1] +' \t ' + str(row[2]))
            print()
        conn.close() 