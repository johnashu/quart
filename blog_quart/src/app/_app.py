from quart import Quart
from app.config import *

blog_app = Quart(__name__)

blog_app.config.update({"SECRET_KEY": SECRET_KEY})
