from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    title: str = None
    text: str = None
    # user: str = None


class PostDB(PostSchema):
    id: int
