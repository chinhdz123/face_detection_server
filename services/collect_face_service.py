import cv2
from ultralytics import YOLO
from repositories.face_repository import db
import face_recognition
import numpy as np
from services.files_service import *
import time
import pickle
from PIL import Image
import io
model_yolo = YOLO("model/best.pt")
#get face


#collect face thresh rieng
def detect_faces_by_yolo(image):
    faces_image = []
    results = model_yolo.predict(image, conf = 0.9)
    for i in range(len(results)):
        boxes = results[i].boxes
        for box in boxes:
            x1,y1,x2,y2 = box.xyxy[0]
            x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
            image_face = image[y1:y2, x1:x2]
            faces_image.append({"image": image_face, "box": [x1,y1,x2,y2]})
    return faces_image

def save_image_from_blob(image_blob, image_path):
    image = Image.open(io.BytesIO(image_blob))
    image.save(image_path)

def get_names_of_face(image,box,num=2):
    x1,y1,x2,y2 =box
    encodings = []
    names = []
    image_know_paths = []
    #mã hóa face
    encoding = face_recognition.face_encodings(image, [(y1,x2,y2,x1)])
    if encoding:
        encoding = encoding[0]
    else:
        return "fail","fail",encoding
    #so sánh mã hóa với dữ liệu lưu trong db
    datas = db.get_all_datas()
    #lấy 3 dữ liệu có dis gần nhất
    for data in datas:
        names.append(data[0])
        bytes_io_object = io.BytesIO(data[1])
        encodings.append(pickle.load(bytes_io_object))
        image = data[2]
        image_path = "statics/images/faces/" + create_random_filename("know") + ".png"
        save_image_from_blob(image, image_path)
        image_know_paths.append(image_path)

    results = face_recognition.compare_faces(encodings, encoding)
    faceDis = face_recognition.face_distance(encodings, encoding)
    for distance in faceDis:
        if distance < 0.5:
            return "fail","fail", encoding

    # Sắp xếp kết quả dựa trên khoảng cách
    sorted_indices = np.argsort(faceDis)
    # Lấy tên của top num kết quả (kiểm tra results trước khi thêm vào top_names)
    top_names = [names[i] for i in sorted_indices if results[i]]
    top_path_images = [image_know_paths[i] for i in sorted_indices if results[i]]
    if len(top_names) >=num:
        top_names = top_names[:num]
        top_path_images = top_path_images[:num]
    return top_names,top_path_images, encoding

def save_face_yaml(face_image, top_names,top_path_images,encoding ):
    face_yaml = yaml2dict("data_detect/face_detect.yaml")
    if not face_yaml:
        face_yaml = []
    name_image = create_random_filename("face") + ".jpg"
    image_path = "statics/images/faces/" + name_image
    cv2.imwrite(image_path, face_image)
    face_dict = {"image_path":image_path, "names": top_names, "encoding": encoding.tolist(), "image_paths":top_path_images}
    face_yaml.append(face_dict)
    dict2yaml(face_yaml, "data_detect/face_detect.yaml")

def collect_face(path):
    cap = cv2.VideoCapture(path)
    start_time = time.time()
    start_time1 = time.time()
    while True:
        _, image = cap.read()
        if _:
            # end_time = time.time()
            # if end_time - start_time > 0.1 :
                # start_time = time.time()
                #detect faces
                faces_image = detect_faces_by_yolo(image)
                #Xem face co trùng ai trong du liệu không (dữ liệu lấy từ db)
                for face in faces_image:
                    top_names,top_path_images, encoding = get_names_of_face(image,face["box"])
                    if top_names != "fail":
                    # if top_names != "fail" and end_time - start_time1 > 2:
                    #     start_time1 = time.time()
                        save_face_yaml(face["image"], top_names,top_path_images, encoding)
                cv2.imshow("a", image)
                cv2.waitKey(1)
        else:
            break

def save_face_to_db(image_path, name):
    with open(image_path, "rb") as f:
        image_blob = f.read()
    face_yaml = yaml2dict("data_detect/face_detect.yaml")
    encodings = []
    indices_to_remove = []

    for face_info in face_yaml:
        if face_info["image_path"] ==image_path:
            encoding = np.array(face_info["encoding"])
        encodings.append(face_info["encoding"])

    results = face_recognition.compare_faces(encodings, encoding)
    faceDis = face_recognition.face_distance(encodings, encoding)
    for i, distance in enumerate(faceDis):
        if distance < 0.5 and results[i]:
            indices_to_remove.append(i)
    for index in reversed(indices_to_remove):
        del face_yaml[index]

    dict2yaml(face_yaml, "data_detect/face_detect.yaml")
    data = (name,pickle.dumps(encoding), image_blob)
    db.create(data)


