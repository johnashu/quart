from app.api.models.post import PostSchema
from app.db import posts, database
import logging as logger


# POSTS
async def post(payload: PostSchema) -> database:
    query = posts.insert().values(payload)
    return await database.execute(query=query)


# GET
async def get(id: int) -> database:
    query = posts.select().where(id == posts.c.id)
    return await database.fetch_one(query=query)


async def get_all() -> database:
    query = posts.select()
    logger.info(query)
    return await database.fetch_all(query=query)


# PUT
async def put(id: int, payload: PostSchema) -> database:
    query = posts.update().where(id == posts.c.id).values(payload).returning(posts.c.id)
    return await database.execute(query=query)


# DELETE
async def delete(id: int) -> database:
    query = posts.delete().where(id == posts.c.id)
    return await database.execute(query=query)
