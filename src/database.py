from datetime import datetime, timezone
from bson import ObjectId
from pymongo import MongoClient
from pymongo.results import InsertOneResult
from pymongo.errors import DuplicateKeyError
import config
from typing import Dict, List, Optional
import models
import random
import string

MONGO_URI = config.MONGO_URI
client = MongoClient(MONGO_URI)
ALPHANUM_TUPLE = tuple(string.ascii_letters + string.digits)

def GetDb():
    return client["database"]

def DoShortenedAttempt():
    shortened = ""

    for i in range(config.SHORTENED_LENGTH):
        shortened += random.choice(ALPHANUM_TUPLE)

    return shortened

def CreateShortenedURL(url : str) -> models.ShortenedURL | None:
    db = GetDb()
    collection = db["urls"]
    now = datetime.now(timezone.utc)

    for _ in range(10):
        attempt = DoShortenedAttempt()
        model = models.ShortenedURL(url = url, short_url = attempt, created_at = now, updated_at = now, access_count = 0)

        try:
            collection.insert_one(model.model_dump())

            return model
        except DuplicateKeyError:
            continue
    
    raise RuntimeError("Unable to generate unique short URL")