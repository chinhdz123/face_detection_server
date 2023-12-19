
from repositories.face_repository import db
from services.files_service import *
from services.collect_face_service import *
from typing import List

async def get_face_infor()-> List[dict]:
    result ={}
    face_yaml = yaml2dict("data_detect/face_detect.yaml")

    listface = []
    if face_yaml:
        for face_info in face_yaml:
            new_face_info = {"image_path": face_info["image_path"], "names": face_info["names"], "image_paths": face_info["image_paths"]}
            listface.append(new_face_info)
    result["listface"] = listface
    return result

async def delete_face(input_data):
    face_yaml = yaml2dict("data_detect/face_detect.yaml")
    new_listface = []
    if face_yaml:
        for face_info in face_yaml:
            if face_info["image_path"] != input_data.image_path:
                new_listface.append(face_info)
    dict2yaml(new_listface, "data_detect/face_detect.yaml")
    return "xóa thành công"

async def delete_all():
    new_listface = []
    dict2yaml(new_listface, "data_detect/face_detect.yaml")
    return "xóa thành công"

async def create_face(input_data):
    name = input_data.name
    image_path = input_data.image_path
    save_face_to_db(image_path, name)
    return "Lưu thành công."
