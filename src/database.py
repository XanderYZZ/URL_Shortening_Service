from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import config
from typing import Dict, Optional
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

def MakeDatetimeAware(doc: Optional[Dict]) -> Optional[Dict]:
    if not doc:
        return doc
    
    if doc.get("created_at") and doc["created_at"].tzinfo is None:
        doc["created_at"] = doc["created_at"].replace(tzinfo=timezone.utc)
    if doc.get("updated_at") and doc["updated_at"].tzinfo is None:
        doc["updated_at"] = doc["updated_at"].replace(tzinfo=timezone.utc)
    
    return doc

def NormalizeURL(url : str) -> str:
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    
    return url

def CreateShortenedURL(url : str) -> models.ShortenedURL | None:
    url = NormalizeURL(url)
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

def GetFullURL(short_url : str, increment_access = False) -> str | None:
    db = GetDb()
    collection = db["urls"]
    result = collection.find_one({"short_url": short_url,})

    if result is None:
        return None
    
    if increment_access:
        collection.update_one({"short_url": short_url,}, {"$inc": {"access_count": 1}})

    url = NormalizeURL(result["url"])

    return url

def UpdateURL(short_url : str, url : str) -> bool:
    db = GetDb()
    collection = db["urls"]
    result = collection.find_one({"short_url": short_url,})

    if result is None:
        return False
    
    url = NormalizeURL(url)
    collection.update_one({"short_url": short_url}, {"$set": {"url": url}}) 

    return True

def GetShortenedURLModel(short_url : str) -> models.ShortenedURL | None:
    db = GetDb()
    collection = db["urls"]
    result = collection.find_one({"short_url": short_url,})
    result = MakeDatetimeAware(result)

    return result

def DeleteShortURL(short_url : str) -> bool: 
    db = GetDb()
    collection = db["urls"]
    result = collection.find_one({"short_url": short_url,})

    if result is None:
        return False 
    
    collection.delete_one({"short_url": short_url})

    return True