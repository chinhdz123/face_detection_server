import cv2
import time
import os
from services.files_service import create_random_filename
from services.collect_face_service import detect_faces_by_yolo
def collect_face(path):
    
    base_name = os.path.basename(path).replace(".")
    output_folder = "tmp\data\images/" + base_name
    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(path)
    start_time = time.time()
    i=0
    while i < 20:
        _, image = cap.read()
        if _:
            end_time = time.time()
            if end_time - start_time > 1 :
                i+=1
                start_time = time.time()
                #detect faces
                faces_image = detect_faces_by_yolo(image)
                #Xem face co trùng ai trong du liệu không (dữ liệu lấy từ db)
                for face in faces_image:
                    output_name = create_random_filename("output") + ".jpg"
                    cv2.imwrite(output_folder+"/"+output_name, face)
                    
                cv2.imshow("a", image)
                cv2.waitKey(1)
        else:
            break
        

path = r"tmp\data\videos\Lê Ngọc Chinh.mp4"
collect_face(path)