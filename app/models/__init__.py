import sys
from inspect import getmembers, isclass
from typing import TypeVar, Type

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from .users import *

DocType = TypeVar("DocType", bound=Document)


def get_models() -> list[Type[DocType]]:
    """ Returns a list of MongoDB Beanie document classes as specified in the `models` module"""
    return [doc for _, doc in getmembers(sys.modules[__name__], isclass)
            if issubclass(doc, Document) and doc.__name__ != "Document"]


async def init_db():
    """
    Initialize the MongoDB database with the Beanie documents defined in the `models` module
    """

    document_models = get_models()
    connection_string = f'{settings.DATABASE_URI}/{settings.DATABASE_NAME}'
    client = AsyncIOMotorClient(connection_string)
    db = client[settings.DATABASE_NAME]
    await init_beanie(db, document_models=document_models)
