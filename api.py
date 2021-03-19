from typing import List
import shutil
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from starlette.requests import Request

from schemas import UploadImage, GetImage, User, Message


image_router = APIRouter()

# @image_router.get("/image")
# async def post_image():
#     return


@image_router.post("/image")
async def post_image(title: str = Form(...), description: str = Form(...), file: UploadFile = File(None)):
    info = UploadImage(title=title, description=description)
    with open(f'media/images/{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_name": file.filename, "info": info}


@image_router.post("/images")
async def post_images(files: List[UploadFile] = File(None)):
    for img in files:
        with open(f'{img.filename}', "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)

    return {"file_name": "Файлы удачно загружены"}


@image_router.get("/image", response_model=GetImage, responses = {404: {"model": Message}})
async def get_image():
    user = User(**{'id': 23, 'name': 'Jordan'})
    image = UploadImage(**{'title': 'Test', 'description': 'Description'})
    # return GetImage(user=user, image=image)
    return JSONResponse(status_code=404, content={"message": "Item not found"})


@image_router.get("/test")
async def get_test(req: Request):
    print(req.base_url)
    return {}