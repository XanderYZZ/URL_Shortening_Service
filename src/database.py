from datetime import datetime, timezone
from bson import ObjectId
from pymongo import MongoClient
from pymongo.results import InsertOneResult
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

def CreateShortenedURL(url : str):
    attempt = ""

    while True:
        attempt = DoShortenedAttempt()

        if not GetDb()["urls"].find({"short_url": attempt}):
            break 
    
    now = datetime.now(timezone.utc)
    new_data = models.ShortenedURL(url, attempt, now, now, 0)
    new_data = {"$set": new_data}

    GetDb()["urls"].update_one({"short_url": attempt}, new_data, upsert=True)