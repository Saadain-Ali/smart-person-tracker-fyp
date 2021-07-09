# from face_encoder import face_encoder
# import time
# f = face_encoder('encodings_Allolf.pickle','dataset/60838','hog')
# f.start()
# # f.join()
# # f.run()
# while(f._running):
#     print(f.imgLen())
#     print(f.imageNumber())
#     time.sleep(2)



# from student import student_info

# std_info = student_info.getData(sid="Saadain")

# print(std_info['sid'])

from info_finder import info_extractor as extract

extract.student_countByID();