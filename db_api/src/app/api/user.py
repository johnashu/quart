from app.api import user_crud
from app.api.models.user import UserSchema, UserDB
from fastapi import APIRouter, HTTPException, Path
from asyncpg.exceptions import UniqueViolationError, DataError
from starlette.responses import JSONResponse
from typing import List
import logging as logger

from app.api.common.error_messages import ERROR_404, ERROR_VALUE_OUT_OF_INT32_RANGE

router = APIRouter()

# USER
@router.post("/", response_model=UserDB, status_code=201)
async def create_user(payload: UserSchema):
    logger.info(payload)
    try:
        user_id = await user_crud.post(payload.__dict__)
    except UniqueViolationError as e:
        return JSONResponse(
            status_code=409, content={"USER already registered": f"{e.as_dict()}"}
        )
    response_object = {**{"id": user_id}, **payload.__dict__}
    return response_object


# GET
@router.get("/{id}/", response_model=UserDB, status_code=200)
async def read_user(id: int = Path(..., gt=0)):

    try:
        user = await user_crud.get(id)
    except DataError:
        ctx = {"Error": ERROR_VALUE_OUT_OF_INT32_RANGE, "id": id}
        return JSONResponse(status_code=404, content=ctx)

    if not user:

        ctx = {
            **{"Error": ERROR_404, "id": id},
        }
        return JSONResponse(status_code=404, content=ctx)

    return user


@router.get("/", response_model=List[UserDB])
async def read_all_user():
    return await user_crud.get_all()


@router.get("/user/{username}/", response_model=UserDB, status_code=200)
async def read_by_user(username: str):
    logger.info(username)
    user_res = await user_crud.get_with_username(username)
    if not user_res:
        ctx = {"Error": ERROR_404, "username": username}
        return JSONResponse(status_code=404, content=ctx)
    response = user_res.__dict__["_row"]
    return response


# PUT
@router.put("/{id}/", response_model=UserDB)
async def update_user(payload: UserSchema, id: int = Path(..., gt=0)):
    user = await user_crud.get(id)

    if not user:
        ctx = {"Error": ERROR_404, "id": id}
        return JSONResponse(status_code=404, content=ctx)

    user_id = await user_crud.put(id, payload)

    response_object = {**{"id": id}, **payload.__dict__}

    return response_object


# DELETE
@router.delete("/{id}/", response_model=UserDB)
async def delete_user(id: int = Path(..., gt=0),):
    user = await user_crud.get(id)
    if not user:
        ctx = {"Error": ERROR_404, "id": id}
        return JSONResponse(status_code=404, content=ctx)
    await user_crud.delete(id)
    return user
