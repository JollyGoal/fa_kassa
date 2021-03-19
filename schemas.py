from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class UploadImage(BaseModel):
    title: str
    description: str


class GetImage(BaseModel):
    user: User
    image: UploadImage


class Message(BaseModel):
    message: str

# class Item(BaseModel):
#     id: int
#     name: str
#     description: str
#     min_per: int
#     max_per: int
#     price: float
#     quantity: int
#     date: str
#     image: str
