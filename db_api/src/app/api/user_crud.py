from app.api.models.user import UserSchema
from app.db import users, database
import logging as logger

# USER
async def post(payload: UserSchema) -> database:
    query = users.insert().values(payload)
    return await database.execute(query=query)


# GET
async def get(id: int) -> database:
    query = users.select().where(id == users.c.id)
    return await database.fetch_one(query=query)


async def get_all() -> database:
    query = users.select()
    return await database.fetch_all(query=query)


async def get_with_username(username: str) -> database:
    query = users.select().where(username == users.c.username)
    logger.info(query)
    return await database.fetch_one(query=query)


# PUT
async def put(id: int, payload: UserSchema) -> database:
    query = users.update().where(id == users.c.id).values(payload).returning(users.c.id)
    return await database.execute(query=query)


# DELETE
async def delete(id: int) -> database:
    query = users.delete().where(id == users.c.id)
    return await database.execute(query=query)
