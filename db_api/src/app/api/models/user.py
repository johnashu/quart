from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str = None
    pword: str = None
    salt: str = None
    # expires: str = None


class UserDB(UserSchema):
    id: int
