from pydantic import BaseModel, Field
from typing import List, Tuple

class Face(BaseModel):
    image_path: str
    names: List[str] 
    image_paths: List[str] 

class ListFace(BaseModel):
    listface:  List[Face]

class SaveFace(BaseModel):
    image_path: str
    name: str

class DeleteInfor(BaseModel):
    image_path: str
