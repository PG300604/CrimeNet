"""
Conductor API initialization
"""
import os
import sys
sys.path.insert(0, os.path.abspath(".."))
import shutil
import ujson
from falcon import API, media
from .src.middlewares.authorization import AuthorizationComponent
from .src.middlewares.multipart import FormComponent
from .src.middlewares.log_middleware import LoggingComponent
from .src.router import VersionedRouter
from .src.config import config
from .src.auth_models import Role, User, AlreadyExistsError
from .src.auth_graph import auth_dataset


def startup():
    """ Create roles and admin user in datastore if they do not exist """
    for i, role in enumerate(config["roles"]):
        try:
            Role(auth_dataset).add_role(role, i)
        except AlreadyExistsError:
            pass
    try:
        User(auth_dataset).store_user(
            config["default_admin"]["username"],
            config["default_admin"]["password"],
            config["roles"][-1])
    except AlreadyExistsError:
        user = User(auth_dataset)
        user.delete(config["default_admin"]["username"])
        user.store_user(
            config["default_admin"]["username"],
            config["default_admin"]["password"],
            config["roles"][-1])
    finally:
        if os.getenv("production") == "true":
            for root, dirs, files in os.walk(config["temp_file_folder"]):
                for folder in dirs:
                    shutil.chown(os.path.join(root, folder), "www-data", "www-data")
                for file in files:
                    shutil.chown(os.path.join(root, file), "www-data", "www-data")


json_handler = media.JSONHandler(
    dumps=ujson.dumps,
    loads=ujson.loads
)

media_handlers = {
    "application/json": json_handler,
    "application/msgpack": media.MessagePackHandler()
}

router = VersionedRouter()

api = API(
    router=router,
    middleware=[
        LoggingComponent(),
        AuthorizationComponent(),
        FormComponent()])

from .src import config_logs
from .src import config_routes
from .src import error_hanlder
from .src import celery

startup()
