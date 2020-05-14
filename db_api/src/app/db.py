import os

from databases import Database

from sqlalchemy import (
    Column,
    DateTime,
    String,
    Boolean,
    MetaData,
    Integer,
    Table,
    Text,
    CheckConstraint,
    create_engine,
)
from sqlalchemy.sql import func

import logging as log

DB_URL = os.getenv("DATABASE_URL")
BLOG_NAME = os.getenv("BLOG_NAME")
DATABASE_URL = DB_URL.format(BLOG_NAME)

stars = "*" * 100

# sqlalchemy
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

metadata_posts = MetaData()
posts = Table(
    "posts",
    metadata_posts,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("text", String()),
    Column("Timestamp", DateTime, default=func.now(), nullable=False),
)

metadata_users = MetaData()
users = Table(
    "users",
    metadata_users,
    Column("id", Integer, primary_key=True),
    Column("username", String, nullable=False, unique=True),
    Column("pword", String(), nullable=False),
    Column("salt", String(), nullable=False),
)

# database query builder
database = Database(DATABASE_URL)
