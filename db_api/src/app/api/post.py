from app.api import post_crud
from app.api.models.post import PostSchema, PostDB
from fastapi import APIRouter, HTTPException, Path
from asyncpg.exceptions import UniqueViolationError, DataError
from starlette.responses import JSONResponse
from typing import List
import logging as logger

from app.api.common.error_messages import ERROR_404, ERROR_VALUE_OUT_OF_INT32_RANGE

router = APIRouter()

# POST
@router.post("/", response_model=PostDB, status_code=201)
async def create_post(payload: PostSchema):
    logger.info(payload)
    post_id = await post_crud.post(payload.__dict__)
    if post_id:
        response_object = {**{"id": post_id}, **payload.__dict__}
        return response_object

    ctx = {
        **{"Error": ERROR_404, **payload.__dict__},
    }
    return JSONResponse(status_code=404, content=ctx)


# GET
@router.get("/{id}/", response_model=PostDB, status_code=200)
async def read_post(id: int = Path(..., gt=0)):

    try:
        post = await post_crud.get(id)
    except DataError:
        ctx = {"Error": ERROR_VALUE_OUT_OF_INT32_RANGE, "id": id}
        return JSONResponse(status_code=404, content=ctx)

    if not post:
        ctx = {
            **{"Error": ERROR_404, "id": id},
        }
        return JSONResponse(status_code=404, content=ctx)
    return post


@router.get("/", response_model=List[PostDB])
async def read_all_post():
    res = await post_crud.get_all()
    if res:
        new_res = []
        for x in res:
            d = dict(x.__dict__["_row"])
            d.update({"Timestamp": d["Timestamp"].strftime("%m/%d/%Y %H:%M:%S")})
            logger.info(d)
            new_res.append(d)
        logger.info(new_res)
        return JSONResponse(status_code=200, content=new_res)
    return res


# PUT
@router.put("/{id}/", response_model=PostDB)
async def update_post(payload: PostSchema, id: int = Path(..., gt=0)):
    post = await post_crud.get(id)
    if not post:
        ctx = {"Error": ERROR_404, "id": id}
        return JSONResponse(status_code=404, content=ctx)
    post_id = await post_crud.put(id, payload)
    if post_id:
        response_object = {**{"id": id}, **payload.__dict__}
        return response_object


# DELETE
@router.delete("/{id}/", response_model=PostDB)
async def delete_post(id: int = Path(..., gt=0),):
    post = await post_crud.get(id)
    if not post:
        ctx = {"Error": ERROR_404, "id": id}
        return JSONResponse(status_code=404, content=ctx)
    await post_crud.delete(id)
    return post
