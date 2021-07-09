class student:

    def __init__(self,Fname,Lname,sid,email,age,gender):
        self.first_name = Fname
        self.last_name = Lname
        self.sid = sid
        self.email = email
        self.age = age 
        self.gender = gender 
    
    def toDictionary(self):
        return  {
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'sid': self.sid ,
            'email' : self.email,
            'age' : self.age,
            'gender' :self.gender
        }
        