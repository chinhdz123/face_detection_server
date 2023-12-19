from fastapi import APIRouter,FastAPI, UploadFile, Form, File
from .schema import *
from controllers import collect_face

router = APIRouter()

@router.get('/get_list_face', response_model = ListFace)
async def food_classification():
    result = await collect_face.get_face_infor()
    return result

@router.post('/delete_face')
async def delete_face(input_data: DeleteInfor):
    result = await collect_face.delete_face(input_data)
    return result

@router.delete('/delete_all')
async def delete_all():
    result = await collect_face.delete_all()
    return result

@router.post('/save_face')
async def food_classification(input_data: SaveFace):
    result = await collect_face.create_face(input_data)
    return result