from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api import post, user
from app.db import engine, metadata_users, database, metadata_posts, BLOG_NAME

from starlette.responses import JSONResponse

# from starlette.exceptions import ProblemException
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

metadata_users.create_all(engine)
metadata_posts.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(post.router, prefix=f"/posts", tags=["posts"])
app.include_router(user.router, prefix=f"/users", tags=["users"])
