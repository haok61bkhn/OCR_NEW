import sys

import uvicorn
from typing import Optional
from fastapi import FastAPI,APIRouter, Request, Depends, File, UploadFile
from pydantic import BaseModel
from io import BytesIO
import numpy as np
from main import OCR_Document
import base64
from PIL import Image
from connector import Connector
import cv2
import uuid
import os


class Item1(BaseModel): 
    data: dict
   

class Item2(BaseModel): 
    image_path: str
    pattern_name : str

# ocr= OCR_Document()
conn=Connector("doc")
dir_image="data_images"

app = FastAPI()


def read_imagefile(data) :
    image = Image.open(BytesIO(data)).convert('RGB') 
    open_cv_image = np.array(image) 
    open_cv_image = open_cv_image[:, :, ::-1].copy() 
    return open_cv_image

def save_image(img):
    print(img.shape)
    try:
        output_path=os.path.join(dir_image,str(uuid.uuid4())+".jpg")
        print(output_path)
        cv2.imwrite(output_path,img)
        return output_path
    except Exception as e:
        print(e)
        return -1


@app.post("/upload/")
async def create_upload_file(image_file : bytes = File(...)):
    img=read_imagefile(image_file)
    output_path = save_image(img)

    if(output_path==-1):
        return {"path":"-1"} # file fail
    else:
        return {"path":output_path}


@app.post("/config/")
async def create_upload_file(data : Item1 ):
  
    id=conn.add_documents(data.data)

    return {"id":id} # id:-1  duplicate pattern_name 

@app.post("/get_infor_doc/")
async def get_infor( item :Item2):
    res={"data": [
        {
        "keyword": "1. nội dung ủy nhiệm",
        "value": "1. nội dung ủy nhiệm",
        "type": "title",
        "score": 0.89
        },
        {
        "keyword": "người ủy nhiệm",
        "value": "Nguyễn Duy Anh",
        "type": "field",
        "score": 0.89
        },
        {
        "keyword": "2. bên ủy quyền",
        "value": "2. bên ủy quyền",
        "type": "field",
        "score": 0.89
        }
        ],
        "alert":
            {
                "is_alert": True,
                "message": "Có dòng bị đè"
            }}
    return res


@app.post("/get_pattern_names/")
async def get_pattern_name():
    
  
    pattern_names=conn.get_pattern_names()

    return {"pattern_names":pattern_names} # id:-1  duplicate pattern_name 


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=1313, log_level="info")
