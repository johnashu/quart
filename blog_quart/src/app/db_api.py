import os
from requests import Session
import logging as logger
import bcrypt

from app._app import blog_app
from app.config import *
from json import dumps

logger.basicConfig(level=logger.DEBUG)

# l
# API_URL = 'http://db_api:5050'


def _post_data(session: Session, url: str, json_data: dict) -> None:
    with session.post(url, json=json_data) as response:
        res = response.json()
        logger.info(res)
        logger.info(response.status_code)
        if response.status_code != 201:
            return False, res
        return True, res


def post_data(url: str, data: dict) -> None:
    with Session() as session:
        res, msg = _post_data(session, url, data)
        return res, msg


def _get_data(session: Session, url: str) -> None:
    with session.get(url) as response:
        res = response.json()
        logger.info(res)
        logger.info(response.status_code)
        if response.status_code != 200:
            return False, res
        return True, res


def get_data(url: str) -> None:
    with Session() as session:
        res, msg = _get_data(session, url)
        return res, msg


def get_user(username: str) -> dict:
    res, msg = get_data(f"{API_URL}/users/user/{username}")
    logger.info(res)
    if not res:
        return False
    return msg


def add_user_to_db(username: str, password: str, salt: str) -> bool:
    data = {"username": username, "pword": password, "salt": salt}

    res, msg = post_data(f"{API_URL}/users/", data)
    logger.info(res)
    if not res:
        return "User already exists"
    return res


def get_posts() -> dict:
    # #loop = asyncio.get_event_loop()
    res, msg = get_data(f"{API_URL}/posts/")
    logger.info(res)
    if not res:
        return False
    return msg


def add_post_to_db(data: dict) -> bool:

    res, msg = post_data(f"{API_URL}/posts/", data)
    logger.info(res)
    if not res:
        return False
    return res


def add_first_superuser() -> None:
    admin = get_user(ADMIN_USER)
    if not admin:
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(ADMIN_PASS.encode("utf8"), salt)
        res = add_user_to_db(ADMIN_USER, str(password, "ascii"), str(salt, "ascii"))
        logger.info(res)


add_first_superuser()
