from os.path import exists, join
from pathlib import Path
from sqlite3 import dbapi2 as sqlite3
from sqlite3 import IntegrityError
from os.path import exists, join
import bcrypt

import logging as logger

from quart import render_template, g, redirect, request, url_for, abort, session, flash

import os

from app._app import blog_app
from app.tools.validate_pass import validate
from app.db_api import *
from app.config import *

logger.basicConfig(level=logger.DEBUG)
logger.basicConfig(
    format="%(asctime)s <%(funcName)s> in <%(module)s> LINE: %(lineno)d -- [%(levelname)s] -- %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    level=logger.INFO,
)


@blog_app.route("/", methods=["GET"])
async def posts() -> render_template:
    bposts = get_posts()
    return await render_template("posts.html", posts=bposts)


@blog_app.route("/", methods=["POST"])
async def create() -> redirect:
    if not session.get("logged_in"):
        abort(401)
    form = await request.form
    data = {
        "title": form["title"],
        "text": form["text"],
    }

    added = add_post_to_db(data)
    if added:
        return redirect(url_for("posts"))
    return redirect(url_for("login"))  # 500 error?


@blog_app.route("/login", methods=["GET", "POST"])
async def login() -> render_template:
    error = None
    if request.method == "POST":
        form = await request.form

        username = form["username"]
        # get info from db
        db_data = get_user(username)
        if db_data:
            db_user = db_data["username"]

            # create hashed pass from form
            salt = db_data["salt"].encode("utf8")
            db_pass = db_data["pword"].encode("utf8")
            logger.info(db_pass)
            logger.info(salt)

            password = bcrypt.hashpw(form["password"].encode("utf8"), salt)

            logger.info(username != db_user)
            logger.info(password != db_pass)
            logger.info(db_pass)
            logger.info(password)
            if username != db_user:
                error = "Invalid username"
            elif password != db_pass:
                error = "Invalid password"
            else:
                session["logged_in"] = True
                await flash("You were logged in")
                return redirect(url_for("posts"))
        else:
            error = "Username Does not exist"
    return await render_template("login.html", error=error)


@blog_app.route("/logout")
async def logout():
    session.pop("logged_in", None)
    await flash("You were logged out")
    return redirect(url_for("posts"))


@blog_app.route("/new_user", methods=["GET", "POST"])
async def new_user() -> render_template:
    error = None
    salt = bcrypt.gensalt()
    if request.method == "POST":
        form = await request.form

        username = form["username"]
        validated = validate(form["password"])
        print(validated)

        password = bcrypt.hashpw(form["password"].encode("utf8"), salt)
        confirm_password = bcrypt.hashpw(form["confirm_password"].encode("utf8"), salt)

        if password == confirm_password:
            if validated == "True":
                new = add_user_to_db(
                    username, str(password, "ascii"), str(salt, "ascii")
                )
                if new == True:
                    session["logged_in"] = True
                    await flash("New User Created. You are now logged in..")
                    return redirect(url_for("posts"))
                else:
                    error = new
            else:
                error = validated
        else:
            error = "Passwords Do Not Match!"
    return await render_template("new_user.html", error=error)


# if __name__ == '__main__':
#     import tools.startup
#     import os
#     # blog_app.run(host='0.0.0.0', port=os.getenv('APP_PORT'), debug=True)
#     blog_app.run(host='0.0.0.0',
#         port=os.getenv('APP_PORT'),
#         certfile='cert.pem',
#         keyfile='key.pem')
