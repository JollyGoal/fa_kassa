from typing import List

import uvicorn as uvicorn
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
from models import UserPydantic, User, UserInPydantic, UserPydanticList, Item,\
    ItemPydantic, ItemInPydantic, ItemPydanticList, Status

app = FastAPI()


######################################################################################################
                                             ##USERS##


"""СПИСОК ЮЗЕРОВ"""
@app.get("/users", response_model=List[UserPydantic])
async def get_users():
    return await UserPydantic.from_queryset(User.all())


"""СОЗДАНИЕ ЮЗЕРА"""
@app.post("/users", response_model=UserPydantic)
async def create_user(user: UserInPydantic):
    user_obj = await User.create(**user.dict(exclude_unset=True))
    return await UserPydantic.from_tortoise_orm(user_obj)


"""ПОИСК ЮЗЕРА ПО ID"""
@app.get(
    "/user/{user_id}", response_model=UserPydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    return await UserPydantic.from_queryset_single(User.get(id=user_id))


"""ИЗМЕНЕНИЕ ЮЗЕРА ПО ID"""
@app.post(
    "/user/{user_id}", response_model=UserPydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: int, user: UserInPydantic):
    await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await UserPydantic.from_queryset_single(User.get(id=user_id))


"""УДАЛЕНИЕ ЮЗЕРА"""
@app.delete("/user/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")

######################################################################################################
                                             ##PRODUCTS##


"""СПИСОК ПРОДУКТОВ"""
@app.get("/items", response_model=List[ItemPydantic])
async def get_items():
    return await ItemPydantic.from_queryset(Item.all())


"""СОЗДАНИЕ ПРОДУКТА"""
@app.post("/items", response_model=ItemPydantic)
async def create_item(item: ItemInPydantic):
    item_obj = await Item.create(**item.dict(exclude_unset=True))
    return await ItemPydantic.from_tortoise_orm(item_obj)


"""ПОИСК ПРОДУКТА ПО ID"""
@app.get(
    "/item/{item_id}", response_model=ItemPydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_item(item_id: int):
    query = Item.get(id=item_id)
    return await ItemPydantic.from_queryset_single(query)


"""ИЗМЕНЕНИЕ ПРОДУКТА ПО ID"""
@app.post(
    "/item/{item_id}", response_model=ItemPydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_item(item_id: int, item: ItemInPydantic):
    await Item.filter(id=item_id).update(**item.dict(exclude_unset=True))
    return await ItemPydantic.from_queryset_single(Item.get(id=item_id))


"""УДАЛЕНИЕ ПРОДУКТА ПО ID"""
@app.delete("/item/{item_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_item(item_id: int):
    deleted_count = await Item.filter(id=item_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return Status(message=f"Deleted item {item_id}")

######################################################################################################
register_tortoise(
    app,
    db_url="sqlite://sql_app.db",
    modules={"models": ["models"], "aerich.models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)