import cv2
import concurrent.futures
import face_recognition
import time
import numpy as np
from student import student_info
import sqlite3


class Capturing ():
    def __init__(self, camera , faceEncodings):
        
        self.nameList = []
        self.camera = camera
        self.isRunning = True

        self.counter = 0
        self.classNames = []

        # load the known faces and embeddings
        print("[INFO] loading encodings...")

        # Loading Encodings from pickel file
        # self.data = pickle.loads(open("encodings_All.pickle", "rb").read())
        self.data = faceEncodings
        self.encodeListKnown = self.data['encodings']

        # testing pickel file data not necessary
        print(len(self.encodeListKnown))
        self.classNames = self.data['names']

        # face recognition with HaarCascade 
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('trainer/trainer.yml')
        self.cascadePath = "haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)

        self.cap =  cv2.VideoCapture(camera)
        self.std_info = []

    def haarReco(self,img):
        # cv2.imshow('camera',img) 
        name = "unknown"
        names =	{
            62445: "saadain",
            62647: "arbaz",
            12345: "ghayaas"
        }
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
        faces = self.faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            #minSize = (int(minW), int(minH)),
        )
        
        for(x,y,w,h) in faces:
            
            
            #cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        
            id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])
            # print("id is " + names[id])
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence <  100):
                name = names[id]
                #confidence = "  {0}%".format(round(100 - confidence))
                
                #print(confidence)
                #print(int(float(confidence.split('%')[0])))
                
                #if(int(float(confidence.split('%')[0])) > 30):
                #    print("Haar reco")
                #    name = names[id]
                    
            else:
                name = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
        
        return name.lower()

    # make it a seperate thread
    def getData(self,sid):
        row = []
        conn = sqlite3.connect('student.db')
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
    # 

    def get_frame(self):
      
        self.current_name  = ""
        self.nameList = []
        success, img = self.cap.read()
        
        # means 1/4th of orignal image
        imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgSmall = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # imgSmall = imutils.resize(img, width=750)
        r = img.shape[1] / float(imgSmall.shape[1])

        # Findig face location and encodes them
        facesCurFrame = face_recognition.face_locations(imgSmall)
        # print(facesCurFrame)
        encodeCurFrame = face_recognition.face_encodings(imgSmall, facesCurFrame)
        # 

        names = []

        # Matching face encodings with the DB
        for encoding,faceLoc in zip(encodeCurFrame,facesCurFrame):
            # attempt to match each face in the input image to our known

            # encodings
            matches = face_recognition.compare_faces(self.data["encodings"], encoding,tolerance= 0.5)

            # print(matches)
            name = "Unknown"
        # 

        # Applying 3 different algorithms to correctly match the encodings with the Database

        # Algo 1 
            if True in matches:

                name1 = "unknown"
                faceDis = face_recognition.face_distance(self.encodeListKnown,encoding)
                # #lowest distance will be our best match
                #print(faceDis)
                minDis = np.min(faceDis)
                matcheIndex = np.argmin(faceDis)
                name1 = self.classNames[matcheIndex]
                print("Algo 1 Matches =  " + name1)
        # Algo 1 ends

        # Algo 2
                name2 = "unknown"
    			# find the indexes of all matched faces then initialize a
    			# dictionary to count the total number of times each face
    			# was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

    			# loop over the matched indexes and maintain a count for
    			# each recognized face face
                for i in matchedIdxs:
                    name2 = self.classNames[i]
                    counts[name2] = counts.get(name2, 0) + 1
    			# determine the recognized face with the largest number
    			# of votes (note: in the event of an unlikely tie Python
    			# will select first entry in the dictionary)
                name2 = max(counts, key=counts.get)
                print("Algo 2 IndexMatching =  " + name2)
                # print("name 2 " +name2)
        # Algo 2 ends

        # Algo 3 Haar Cascade
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self.haarReco, img)
                    return_value = future.result()
                    print("Algo 3 Haar Cascade =  " + return_value)
                    # print(return_value)
                    haarName = return_value
                # haarName = self.haarReco(img)
                # print("haarName = " + haarName )
        # Algo 3 ends 

        #Compairing 
        # if all three name , name2 and name3 has the same name than its a perfect match
                # if name1.lower() == name2.lower() or haarName == name1.lower():
                if name1.lower() == name2.lower() or haarName == name2.lower():
                    print("all match match")
                    name = name1
                    if(name != "unknown"):
                        result = self.getData(sid=name) # sometimes code returns NONE so we are making sure
                        if result:
                            std_info = result
                        # print(std_info)
            names.append(name)
            self.nameList = names
        #======================End Compare==============================================================#
        #
            # Fetching DATA
        
        #
        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(facesCurFrame, names):
    		# rescale the face coordinates
            top = int(top * r)
            right = int(right * r)
            bottom = int(bottom * r)
            left = int(left * r)
            # draw the predicted face name on the image
            cv2.rectangle(img, (left, top), (right, bottom),(0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(img, name.upper(), (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
            # if(name.upper() != "UNKNOWN"):
            #     cv2.putText(img, std_info['sid'], (right+100, bottom+20), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
        #================================================================================================ #
        std_info=[]
        # for orignal
        # ret, jpeg = cv2.imencode('.jpg', image)
        ret, jpeg = cv2.imencode('.jpg', img)
        return self.nameList , jpeg.tobytes()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        # self.recordingThread.stop()
        self.cap.release()

