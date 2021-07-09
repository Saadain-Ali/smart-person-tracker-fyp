import os
from database.Database import info_extractor
from database.student_info import data_handle
from datetime import datetime
import cv2
import concurrent.futures
import face_recognition
import numpy as np
from sklearn import svm


class Capturing ():
    def __init__(self,location ,camera , faceEncodings,tolerance = 0.5):
        
        self.nameList = []
        self.camera = camera
        self.isRunning = True
        self.isError = False

        self.location = location
        self.counter = 0
        self.classNames = [] #to store name in encodings
        self.prev_time = None
        self.prev_name = []

        if self.prev_time == None:
            self.prev_time = str(datetime.now().strftime("%H:%M:%S"))

        # load the known faces and embeddings
        print("[INFO] loading encodings...")

        # Loading Encodings from pickel file
        # self.data = pickle.loads(open("encodings_All.pickle", "rb").read())
        
        #this contains encodings [names,encondings]
        self.data = faceEncodings 
        
        #All Encodigs
        self.encodeListKnown = self.data['encodings']
        
        # All Names
        self.classNames = self.data['names']

        #Tolerance
        self.tolerance = tolerance
        
        # testing pickel file data not necessary
        print(len(self.encodeListKnown))
        
        self.student_list = info_extractor.student_All()
        
        try:
            # face recognition with HaarCascade 
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.read('encodings/trainer.yml')
            self.cascadePath = "cascades/haarcascade_frontalface_default.xml"
            self.faceCascade = cv2.CascadeClassifier(self.cascadePath)


            self.clf = svm.SVC(gamma='scale')
            self.clf.fit(self.encodeListKnown,self.classNames)
        except OSError as identifier:
            print(str(identifier))
            self.isError = True
            return False
        try:
            self.cap =  cv2.VideoCapture(self.camera)
            if self.cap is None or not self.cap.isOpened():
                print('Warning: unable to open video source: ', self.camera)
                self.isError = True
                return False
        except EnvironmentError as identifier:
            print(identifier)
            self.isError = True
            return False
            
        self.make_480p()
        # self.rescale_frame()




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

    def get_frame(self):

        self.nameList = []
        ret , img = self.cap.read()

        if ret == False or self.isError:
            print("frame ends")
            self.stop()
            img = cv2.imread('static/images/no-camera.jpg')
            ret, jpeg = cv2.imencode('.jpg', img)
            return 0 , jpeg.tobytes() , False
        else:           
            img = self.rescale_frame(img)
            
            # means 1/4th of orignal image
            imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgSmall = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # imgSmall = imutils.resize(img, width=750)
            r = img.shape[1] / float(imgSmall.shape[1])

            # Findig face location and encodes them
            facesCurFrame = face_recognition.face_locations(imgSmall)
            encodeCurFrame = face_recognition.face_encodings(imgSmall, facesCurFrame)
            # 

            names = []

            # Matching face encodings with the DB
            for encoding,faceLoc in zip(encodeCurFrame,facesCurFrame):
                # attempt to match each face in the input image to our known

                # encodings
                matches = face_recognition.compare_faces(self.encodeListKnown, encoding,tolerance= self.tolerance)
                name = "Unknown"
            # 

            # Applying 3 different algorithms to correctly match the encodings with the Database

            # Algo 1 
                # #lowest distance will be our best match

                if True in matches:
                    name1 = "unknown"
                    faceDis = face_recognition.face_distance(self.encodeListKnown,encoding)
                    matcheIndex = np.argmin(faceDis)
                    name1 = self.classNames[matcheIndex]
                    print("Algo 1 Matches =  " + name1)
            # Algo 1 ends

            # Algo 2
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face was matched

                    name2 = "unknown"
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name2 = self.classNames[i]
                        counts[name2] = counts.get(name2, 0) + 1
                    
                    # determine the recognized face with the largest number of votes 
                    # (note: in the event of an unlikely tie Python will select first entry in the dictionary)
                    name2 = max(counts, key=counts.get)
                    print("Algo 2 IndexMatching =  " + name2)
            # Algo 2 ends

            # Algo 3 Haar Cascade

                    # with concurrent.futures.ThreadPoolExecutor() as executor:
                    #     future = executor.submit(self.haarReco, img)
                    #     return_value = future.result()
                    #     print("Algo 3 Haar Cascade =  " + return_value)
                    #     # print(return_value)
                    #     haarName = return_value
                
                    haarName = self.clf.predict([encoding])
                    print('svm = ' ,end='' )
                    print(*haarName)
                    # haarName = *haarNa
                    # without  threads
                    # return_value = self.haarReco(img)
                    # print("Algo 3 Haar Cascade =  " + return_value)
                    # haarName = return_value

            # Algo 3 ends 

            #Compairing 
            # if all three name , name2 and name3 has the same name than its a perfect match
                    # if name1.lower() == name2.lower() or haarName == name1.lower():
                    
                    if name1.lower() == name2.lower() or haarName == name2.lower():
                        print("all match match")
                        name = name1
                        
                names.append(name)
                self.nameList = names
            #======================End Compare==============================================================#
            #
                # attendance logic
            self.add_info(self.nameList,self.location)

                # Fetching DATA
                # pehle se saray students ka data rakhlo for fast execution
            #
            # loop over the recognized faces
            for ((top, right, bottom, left), name) in zip(facesCurFrame, names):
                # rescale the face coordinates
                top = int(top * r)
                right = int(right * r)
                bottom = int(bottom * r)
                left = int(left * r)

                if name.upper() == 'unknown'.upper():
                    cv2.rectangle(img, (left, top), (right, bottom),(0,0, 255), 2)
                    b = top - 15 if top - 15 > 15 else top + 15
                    cv2.putText(img, name.upper(), (left, b), cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 0, 255), 2)
                    
                #Saving unknown Faces
                    # generate matrix and compare x y values of mouse click and print name
                    # ================== To handle unknown face =====================#
                    # if self.prev_name.upper() != "UNKNOWN":
                    print('Unknown face is detected')
                    path = os.getcwd() + "/dataset/unknown"
                    cropped = img[top:bottom, left:right]
                    # cv2.imshow("crop",cropped)
                    uname = f'{self.location}_{str(datetime.now())}'
                    cv2.imwrite( path + "/frame" + uname + ".jpg",cropped)
                # ============================================================== #
            
                else:
                # draw the predicted face name on the image
                    cv2.rectangle(img, (left, top), (right, bottom),(0, 255, 255), 2)
                    b = top - 15 if top - 15 > 15 else top + 15
                    y = bottom - 15 if bottom - 15 < 15 else bottom + 15
                    cv2.putText(img, name.upper(), (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 0, 255), 2)
                    for student in self.student_list:
                        if name in str(student[0]):
                            cv2.putText(img, student[1], (left, b), cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 255 ,0), 2)
                            cv2.putText(img, student[2], (right, bottom - 60), cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 255 ,0), 2)
                            cv2.putText(img, student[4], (right, bottom - 30), cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 255 ,0), 2)
                            cv2.putText(img, student[5], (right, bottom ), cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 255, 0), 2)
                            # break
                            # self.stop()
                # if(name.upper() != "UNKNOWN"):
                #     cv2.putText(img, self.std_info['sid'], (left+100, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)

            (H, W) =  img.shape[:2]
            cv2.putText(img, self.location, (10, H - 30),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(img, 'People # '+ str(len(names)), (10, H - 60),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)  
            # cv2.namedWindow(str(self.location), cv2.WINDOW_NORMAL)
            # cv2.imshow(str(self.location), img) 
            # Program will terminate when 'q' key is pressed 
            key = cv2.waitKey(1) & 0xFF

            # if key == ord('q'): 
            #     # break
            #     self.stop()
            #     # ====== Crop Code ====== 
            # elif key == ord("c"):
            #     cropped = img
            #     cv2.imshow("cropped",cropped)
            #     path = os.getcwd() + "/dataset/cropped"
            #     # write karado image
            #     cv2.imwrite(f'{path}/cropped_{self.location}_{str(datetime.now())}',cropped)
            
            # #================================================================================================ #
            # cv2.setMouseCallback(str(self.location), self.click_event,param=[img,self.prev_name])
            
            ret, jpeg = cv2.imencode('.jpg', img)
            return self.nameList , jpeg.tobytes() , True
    # return True

    def stop(self):
        self.isRunning = False
        self.cap.release()

    def __del__(self):
        # self.recordingThread.stop()
        self.stop()
        self.cap.release()
        # cv2.destroyAllWindows()
        # self.cap.release()

    def make_1080p(self):
        self.cap.set(3, 1920)
        self.cap.set(4, 1080)
    
    def make_720p(self):
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
    
    def make_480p(self):
        self.cap.set(3, 640)
        self.cap.set(4, 480)
    
    def change_res(self,width, height):
        self.cap.set(3, width)
        self.cap.set(4, height)
    
    # this one is for scalling a single frame
    def rescale_frame(self,frame, percent=75):
       width = int(frame.shape[1] * percent/ 100)
       height = int(frame.shape[0] * percent/ 100)
       dim = (width, height)
       return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)   
    # ===================================================
    
    
# to handle click events
    def click_event(self,event, x, y, flags,param):
        img = param[0]
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x,', ' ,y)
            font = cv2.FONT_HERSHEY_SIMPLEX
            # strXY = str(x) + ', '+ str(y)
            cv2.putText(param[0], str(param[1]), (x, y), font, .5, (255, 255, 0), 2)
            cv2.imshow(self.location, img)
        if event == cv2.EVENT_RBUTTONDOWN:
            blue = img[y, x, 0]
            green = img[y, x, 1]
            red = img[y, x, 2]
            font = cv2.FONT_HERSHEY_SIMPLEX
            strBGR = str(blue) + ', '+ str(green)+ ', '+ str(red)
            cv2.putText(img, strBGR, (x, y), font, .5, (0, 255, 255), 2)
            cv2.imshow(self.location, img)
        # end click events




    def add_info(self,stdn_list , loc):
        current_name = stdn_list
        print("The currents name are :  ",end='')
        print(current_name)
        # current_name ko sort karna
        if current_name == self.prev_name and len(current_name)>0:
            time_now = str(datetime.now().strftime("%H:%M:%S"))
            
            # taking diff of current and prev time
            diff = datetime.strptime(time_now, "%H:%M:%S") - datetime.strptime(self.prev_time, "%H:%M:%S")

            result = diff.seconds
            print(result)

            if result >= 20:
                self.prev_name = []
                self.prev_time = ""
                print("resetting time")
        elif current_name != self.prev_name and len(current_name)>0:
            self.prev_name = current_name
            # You could also pass datetime.time object in this part and convert it to string.
            self.prev_time = str(datetime.now().strftime("%H:%M:%S")) 
            if(len(stdn_list)==1 and "Unknown" in stdn_list):#if there is only unknown in list
                return 0
            x = np.array(stdn_list)
            students = np.unique(x)
            time = datetime.now().strftime("%H:%M:%S")
            day = datetime.now().strftime("%d-%m-%Y")
            if len(students) > 1 :
                for i in students:
                    if "Unknown" == i:
                        continue
                    for j in students:
                        if i != j:
                            std_info = data_handle(i,j,loc,day,time )
                            std_info.found()
                            std_info.store_to_DB()
            else:
                std_info = data_handle(students[0],"",loc,day,time )
                std_info.found()
                std_info.store_to_DB()
            return 1 