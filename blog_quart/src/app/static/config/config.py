from os.path import join

DB_NAME = join("sql", "blog.db")
SQL_SCHEMA = "schema.sql"
SECRET_KEY = "development"

ADMIN_USER = "admin"
ADMIN_PASS = "default123ABC!@#"

__all__ = ["DB_NAME", "SQL_SCHEMA", "SECRET_KEY", "ADMIN_USER", "ADMIN_PASS"]
