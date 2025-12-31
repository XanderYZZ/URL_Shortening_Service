from fastapi import HTTPException, status, APIRouter
import database
import models

router = APIRouter(tags=["shorten"], prefix="/shorten")

@router.post("/{url}", response_model=models.ShortenedURL)
def CreateShortenedURL(
    url: str,   
):
    result = database.CreateShortenedURL(url)

    if result is None:
        return {"message": "Failed to create!"}
    
    return result