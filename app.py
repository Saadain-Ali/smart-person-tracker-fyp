import pickle
import os
import sqlite3
from face_encoder import face_encoder
import math
from students_editor import students_editor
from student import student
from student import student_info as info
from datetime import datetime
from static.model.location import location

# for stats
from database.Database import info_extractor as database


# weather
import static.model.weather as weather

import numpy as np 
from numpy.core.numeric import count_nonzero

from cam import Capturing
from webcam import RecordingThread, WebCamera
from camera import VideoCamera
from recognizer import Capturing as detector


from flask import Flask, render_template, request, redirect, url_for, flash ,jsonify,g,session,url_for

from flask_ngrok import run_with_ngrok

from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.exc import SQLAlchemyError


# admin data
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='saadain', password='saadi123'))
users.append(User(id=2, username='arbaz', password='arbaz123'))
users.append(User(id=3, username='admin', password='admin'))

# end admin




app = Flask(__name__)
run_with_ngrok(app)


vcam       = None
cameraCount = 0 # to count connected cameras
cam_frame = None
video_camera = None
global_frame = None
g_frame = None
prev_time = None
prev_name = ""
current_name = ""
count = 0

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database/student.db"))

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

locations = {
    "Corridor1" : 0,
    "Corridor2" : 1,
    "Lab1" : 2,
    "Lab2" : 3,
    "Lab3" : 4,
    "Cafe1" : 'http://192.168.0.11:8080/video',
    "Cafe2" :"http://192.168.43.224:8080/video",
    "GateIn" : "http://192.168.0.14:8080/video",
    "GateOut" : 'http://192.168.0.21:8080/video'
    }

activeEncodings = "encodings\encodings_fyp-2_final-hog.pickle";

data = pickle.loads(open(activeEncodings, "rb").read())

class Student(db.Model):
    sid = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80),nullable=False)
    gender = db.Column(db.String(80),nullable=False)
    age = db.Column(db.String(80),nullable=False)
    
    def __init__(self,sid,first_name,last_name,email,gender,age): 
        self.sid =  sid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.age = age


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user_id', None)
    if request.method == 'POST':
        session.pop('user_id', None)
        print('post is here')

        username = str(request.form['username']).lower()
        password = str(request.form['password'])
        
        # user = [x for x in users if x.username == username][0]

        for x in users:
            if x.username == username and x.password == password:
                session['user_id'] = x.id
                return redirect(url_for('Index'))
        return redirect(url_for('login', error  = 'Login Required'))

    return render_template('login.html' , error = 'Login Required')




#This is the index route where we are going to
#query on all our employee data
@app.route('/', methods = ['GET', 'POST'])
def Index():
    if  g.user == None:
        return redirect(url_for('login', error  = 'Login Required'))
    all_data = Student.query.all()
    weath = weather.getTemp()
    # weath = 34
    return render_template("index.html", employees = all_data , username = g.user.username , weather = weath)


# Stats Route
@app.route('/stats', methods = ['GET', 'POST'])
def Stats():
    if  g.user == None:
        return redirect(url_for('login', error  = 'Login Required'))
    all_data = Student.query.all()
    return render_template("stats.html",students = database.student_All() , locations = locations)

# Login
# @app.route('/login', methods = ['GET', 'POST'])
# def login():
#     return render_template("login.html")


# for charts
@app.route('/charts')
def charts():
    if  g.user == None:
        return redirect(url_for('login', error  = 'Login Required'))
    data = {'62445' : 'Hours per Day', 'Lab1' : 11, 'Lab2' : 2, 'Corridor1' : 2, 'Gatein' : 1, 'GateOut' : 1}
	#print(data)
    return render_template('charts.html', data=data , title='62445 occurence')


@app.route('/surv', methods = ['GET', 'POST'])
def surv():
    if  g.user == None:
        return redirect(url_for('login', error  = 'Login Required'))
    activeLocations = {
    "Corridor1" : 0,
    "Corridor2" : 1,
    }
    all_data = Student.query.all()
    return render_template("surv2.html", employees = all_data , locations = activeLocations , title = 'Surv')

# for ip cams
@app.route('/surv_ip', methods = ['GET', 'POST'])
def surv_ip():
    if  g.user == None:
        return redirect(url_for('login', error  = 'Login Required'))
    activeLocations = {
    # "Corridor1" : 0,
    # "Corridor2" : 1,
    # "Lab3" : 4,
    "Cafe2" :"http://192.168.43.224:8080/video",
    }
    all_data = Student.query.all()
    return render_template("surv2.html", employees = all_data , locations = activeLocations ,title = 'Surv-ip')



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        sid = request.form["sid"]              
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        gender = request.form["gender"]
        age = request.form["age"]

        try:
            my_data = Student(sid,first_name,last_name,email,gender,age)
            db.session.add(my_data)
            db.session.commit()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            flash(error)
        
        

        return redirect(url_for('Index'))


#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET','POST'])
def update():
    if request.method == 'POST':
        my_data = Student.query.get(request.form.get('oldSid'))
        my_data.sid = request.form["oldSid"]              
        my_data.first_name = request.form["first_name"]
        my_data.last_name = request.form["last_name"]
        my_data.email = request.form["email"]
        my_data.gender = request.form["gender"]
        my_data.age = request.form["age"]

        db.session.commit()
        flash("Student Updated Successfully")

        return redirect(url_for('Index'))


#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Student.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")

    return redirect(url_for('Index'))

counter = 0
f=None
@app.route('/trainer', methods = ['GET','POST'])
def trainer():
    
    global counter
    global f
    if f is None:
        f = face_encoder(activeEncodings,'dataset','hog')
        f.start()
    if request.method == 'POST':
        json = request.get_json()
        status = json['status']
        print("status "+ status)
        if status == "true" and f._running:
            print(f.imgLen())
            print(f.imageNumber())
            name = f.getImgName()
            print(name)
            counter = (f.imageNumber()/f.imgLen())*100
            print(math.trunc(counter))
            # if counter == 0.0:
            #     print('stoposaafssaaaaa')
            #     return jsonify(value="-1")
            if counter > 100:
                return jsonify(value="100")
            else:
                return jsonify(value = math.trunc(counter) , name = name)
        else:
            return jsonify(value="-1")
    
    
    # f.run()
    return render_template("trainer.html",student ='Saadain')


@app.route('/std_info', methods = ['GET','POST'])
def std_info():
    if request.method == 'POST':
        json = request.get_json()
        std_name = json['name']
        print("name "+ std_name)
        # search db fod std_name information and return
        # if db return values then proceed:
            # return json object of the student's information
        # else:
            # return json object with 0 means stdent not found in db
        return jsonify(info = "True , data not found")
    return render_template("student_info.html",student ='None') #if req is GET then return none and handle on page


@app.route('/record_status', methods=['POST'])
def record_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera(locations['Corridor1'])

    json = request.get_json()

    status = json['status']
    print(json)
    

    if status == "true":
        print('Starting Camera for recording')
        folderName = json['name']
        video_camera.start_record(folderName)
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        video_camera.stop()
        
        print('stopping recorder')
        return jsonify(result="stopped")

def cam_stream(location):
    vcam = None
    global cam_frame
    global current_name
    global prev_name
    global prev_time
    global cameraCount

    if prev_time == None:
        prev_time = str(datetime.now().strftime("%H:%M:%S"))
    print('loadings camera')
    camName =  location #'Corridor1'
    cameraNumber = locations[location]
    print(cameraNumber)
    if vcam == None:
        vcam = detector(camName,cameraNumber,data,0.5)
        cameraCount = cameraCount + 1
    while True:
        name , frame , isRunning = vcam.get_frame()
        
        # if camera disconnects
        if isRunning == False:
            vcam = None
            print('camera disconnects')
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            break
        # if camera available
        else:
            current_name = name
            print("the name is : ")
            print(current_name)

            if current_name != prev_name and len(current_name)>0:
                add_info(current_name,camName)
                prev_name = current_name
                # You could also pass datetime.time object in this part and convert it to string.
                prev_time = str(datetime.now().strftime("%H:%M:%S")) 
            elif current_name == prev_name and  len(current_name)>0:         
                time_now = str(datetime.now().strftime("%H:%M:%S"))
                diff = datetime.strptime(time_now, "%H:%M:%S") - datetime.strptime(prev_time, "%H:%M:%S")            
                # Get the time in hours i.e. 9.60, 8.5
                result = diff.seconds
                print(result)
                if result >= 20:
                    prev_name=[]
                    prev_time = ""
                    print("resetting time")
                
                

            current_name = []
            if frame != None:
                cam_frame = frame
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                yield (b'--frame\r\n'
                                b'Content-Type: image/jpeg\r\n\r\n' + cam_frame + b'\r\n\r\n')

@app.route('/webcam/<location>')
def webcam(location):
    return Response(cam_stream(location),mimetype='multipart/x-mixed-replace; boundary=frame')

def webcam_stream():
    # global video_camera 
    global g_frame
    
    # if video_camera == None:
    # video = cv2.VideoCapture(0)
    recordingThread = RecordingThread("Video Recording Thread", activeEncodings)
    recordingThread.start()
        # video_camera = WebCamera()
        
    while True:
        # frame = video_camera.get_frame()
        frame = recordingThread.get_frame()

        if frame != None:
            g_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + g_frame + b'\r\n\r\n')

# ============= video viewer ==============
@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def video_stream():
    global video_camera 
    global global_frame
    global current_name
    global count

    if video_camera == None:
        video_camera = VideoCamera(locations['Corridor1'])
        
    while True:
        frame = video_camera.get_frame()
        # current_name = "bane"+ str(count)
        # count = count +  1
        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                            b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')
# ========= video viewer end  ==============

@app.route('/getName',methods=['POST'])
def getName():
    # global video_camera 
    # if video_camera == None:
    #     video_camera = VideoCamera()

    json = request.get_json()

    status = json['status']
    print("status "+ status)
    if status == "true":
        print(prev_name)
        row = []
        if prev_name:
            conn = sqlite3.connect('student.db')
            # print("Opened database successfully")
            cursor = conn.execute("SELECT first_name,last_name,sid,email,age,gender From student WHERE first_name = " + '"' + prev_name[0] + '"')
            row = cursor.fetchone()
            conn.close()
            return jsonify(name= row)
        return jsonify(name = "")
        
    else:
        return jsonify(name="")


def add_info(stdn_list , loc):
    if(len(stdn_list)==1 and "Unknown" in stdn_list):
        return 0
    x = np.array(stdn_list)
    students = np.unique(x)
    time = datetime.now().strftime("%H:%M:%S")
    day = datetime.now().strftime("%d-%m-%Y")
    if len(students) > 1 :
        for i in students:
            for j in students:
                if i != j:
                    std_info = info(i,j,loc,day,time )
                    std_info.found()
    else:
        std_info = info(students[0],"",loc,day,time )
        std_info.found()
    return 1 


@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html")



# ======================= S T A T S  =======================
# find max occurence of a student
@app.route("/findMax" , methods=['POST'])
def findMax():
    # print("it on ")
    results = []
    user =  request.form['username']
    # 62445	Saadain	Lab1	2	4.0
    data = database.student_maxOccur(user)
    # print(data)
    if len(data) > 0:
        results = list(data)
        return jsonify(status="OK",results = results)
    return jsonify(status="BAD",results = [])


# last seen
@app.route("/stdsLastSeen" , methods=['POST'])
def stdsLastSeen():
    print("Last Seen ")
    friends = []
    user =  request.form['username']
    date = request.form['date']
    print(user)
    current_date = date
    # current_date = datetime.now().date().strftime("%d-%m-%Y")
    print(current_date)
    data= database.find_lastSeen(user,date = current_date)
    print(data)
    if data != None:
        friends = list(data)
        print("name is " + str(data[1]))
        return jsonify(status="OK",friends = friends)
    return jsonify(status="Bad")
    # return json.dumps({'status':'OK','user':user,'name':name})


@app.route('/findFriend', methods=['POST'])
def findFriend():
    friends = []
    sid = request.form['sid']
    print('sid ' + sid)
    if sid:
        data = database.findStudentFreinds(sid)
        for friend in data:
            friends.append(list(friend))
            print(list(friend))
        return jsonify(friends = friends ,status = 'OK')
    return jsonify( error = 'Missing data!' )

# findAllFreinds'
@app.route('/findAllFreinds', methods=['POST'])
def findAllFreinds():
    sid = request.form['sid']
    # print(email + ' ' + name)
    if sid:
        current_date = datetime.now().date().strftime("%d-%m-%Y")
        data = database.findAllFreinds(sid,current_date)
        if(len(data) <= 0 ):
            return jsonify(error = data )
        return jsonify(results = data ,status = 'OK')
    return jsonify( error = 'Not Found!' )


# most occurence of all students at one plave
@app.route('/findAllAtOneLocation', methods=['POST'])
def findAllAtOneLocation():
    result = []
    location = request.form['location']
    print('location ' ,location)
    # print(email + ' ' + name)
    if location:
        # [ (Haleem | 62987 | Ayaz | 62424 | 1 |) , () ]
        data = database.findAllatOnePlace(location=location)
        for row in data:
            result.append(list(row))
            print(list(row))
        if len(result) > 0:
            return jsonify(result = result , status = 'OK')
    return jsonify(error = 'Missing data!',status = 'BAD')


# Find where with friend
@app.route('/findFriendOccur', methods=['POST'])
def findFriendOccur():
    result = []
    sid1 = request.form['sid1']
    sid2 = request.form['sid2']
    print(f'sid1 {sid1} sid2 {sid2}')
    
    '''
    [(Saadain	Arbaz	Corridor1	16),
    (Saadain	Arbaz	Lab1	2),
    (Saadain	Arbaz	Lab6	1)]
    '''
    
    data = database.findFriendOccur(sid1,sid2)
    print(data)
    if data != None or data != [] or len(data)>0:
        results = list(data)
        print(results)
        return jsonify(status="OK",friends = results)
    return jsonify(status="Bad",friends = [])

@app.route('/findRoute', methods=['POST'])
def findRoute():
    result = []
    sid = request.form['sid']
    date = request.form['date']
    print(f'sid {sid} date {date} ')
    # print(email + ' ' + name)
    
    # Saadain   62445 16-12-2020 GateIn    00:13:32
    # Saadain   62445 16-12-2020 Corridor1 00:13:43
    # Saadain   62445 16-12-2020 GateOut   01:39:40
    data = database.findRoute(sid,date)
    if data != None or data != [] or len(data)>0:
        for row in data:
            result.append(list(row))
            print(list(row))
        return jsonify(result = result , status = 'OK')
    return jsonify(error = 'Missing data!',status = 'BAD')

# in out time
@app.route('/findClockedInOut', methods=['POST'])
def findClockedInOut():
    # result = []
    sid = request.form['sid']
    date = request.form['date']
    # date = request.form['date']
    print(f'sid {sid} {date}')
    # print(email + ' ' + name)
    if sid:
    # 62445 18-12-2020 18:45:57 Corridor1 22:20:41 Corridor1
        # current_date = '18-12-2020'
        if date:
            current_date = date
        else:
            current_date = datetime.now().date().strftime("%d-%m-%Y")
        print(f'currentDate {current_date}')
        result = database.findClockedInOut(sid,str(current_date))
        print(result)
        if (result is not None ) or result != [] or len(result)>0:
            return jsonify(result = result , status = 'OK')
    return jsonify(error = 'Missing data!',status = 'BAD',result = [])



# @app.route('/findClockedmulti', methods=['POST'])
# def findClockedmulti():
#     # result = []
#     sid=[]
#     sid.add(request.form['sid1'])
#     sid.add(request.form['sid2'])
#     sid.add(request.form['sid3'])
   
#     date = request.form['date']
#     # date = request.form['date']
#     # print(f'sid {sid} {date}')
#     # print(email + ' ' + name)
#     if sid[0] and sid[1] and sid[2]:
#     # 62445 18-12-2020 18:45:57 Corridor1 22:20:41 Corridor1
#         # current_date = '18-12-2020'
#         if date:
#             current_date = date
#         else:
#             current_date = datetime.now().date().strftime("%d-%m-%Y")
#         print(f'currentDate {current_date}')
        
#         result = [[0],[0],[0]]
#         for x in range(0, 3):
#             sid = str('sid'+str(x+1))
#             print(sid)
#             result[x] = database.findClockedInOut(sid[0],str(current_date))
#         print(result)
#         if (result is not None ) or result != [] or len(result)>0:
#             return jsonify(result = result , status = 'OK')
#     return jsonify(error = 'Missing data!',status = 'BAD',result = [])


@app.route('/getFinds', methods=['POST'])
def getFinds():
    # result = []
    status =request.form.get('status')
    if status == 'OK':
        result = database.getFindsData()
        if (result is not None ) or result != [] or len(result)>0:
            return jsonify(result = result , status = 'OK')
    return jsonify(error = 'Missing data!',status = 'BAD',result = [])


# ================== S T A T S - - E N D ===================



# =============== DASHBOARD DATA ======================
@app.route('/getDashboardData')
def getDashboardData():
    result = database.getDashboardData()
    result['occurencesToday'] = database.getTotalOccurencesToday()[0]
    result['occurences'] =database.getTotalOccurences()[0]
    result['location'] = 7
    print('hello/////////////////')
    return jsonify(data = result , status = 'OK')
# =============== DASHBOARD DATA ENDS ======================

# ===================== CHARTS DATA =====================
@app.route('/getMostVisitedLocation')
def getMostVisitedLocation():
    result = database.getMostVisitedLocation()
    print(result)
    return jsonify(data = result , status = 'OK')


@app.route('/getHeatMapofOccurences')
def getHeatMapofOccurences():
    result = database.getHeatMapofOccurences()
    print(result)
    return jsonify(data = result , status = 'OK')

    
@app.route('/getTimeLineByLocation')
def getTimeLineByLocation():
    result = database.getTimeLineByLocation('01-01-2021','62445')
    print(result)
    return jsonify(data = result , status = 'OK')



# ===================== CHARTS DATA END=====================
if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True)