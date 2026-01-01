from fastapi import HTTPException, status, APIRouter
from fastapi.responses import RedirectResponse
import database
import models

router = APIRouter(tags=["shorten"], prefix="/shorten")

@router.post("/{url}", response_model=models.ShortenedURL, status_code=status.HTTP_201_CREATED)
def CreateShortenedURL(
    url: str,   
):
    result = database.CreateShortenedURL(url)

    if result is None:
        raise HTTPException(status_code=400, detail="Could not create a shortened url.")
    
    return result

@router.get("/{short_url}", response_class=RedirectResponse)
def GetFullURL(
    short_url: str,
):
    result = database.GetFullURL(short_url, True)

    if result is None:
        raise HTTPException(status_code=404, detail="Short url does not exist in the database.")
    
    return RedirectResponse(
        url=result,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT
    )

@router.get("/{short_url}/stats", response_model=models.ShortenedURL, status_code=status.HTTP_200_OK)
def GetStats(
    short_url: str
):
    result = database.GetShortenedURLModel(short_url)

    if result is None:
        raise HTTPException(status_code=404, detail="Short url does not exist in the database.")
    
    return result

@router.put("/{short_url}", status_code=status.HTTP_200_OK)
def UpdateShortURL(
    short_url: str,
    data: models.UpdateURLRequest,
):
    result = database.UpdateURL(short_url, data.url)

    if result is False or result is None:
        raise HTTPException(status_code=400, detail="Could not update the url entry.")   
    
    return {"message": "You updated the full url for " + short_url + " to " + data.url}
    
@router.delete("/{short_url}", status_code=status.HTTP_204_NO_CONTENT)
def DeleteShortURL(
    short_url: str
):
    result = database.DeleteShortURL(short_url)

    if result is False or result is None:
        raise HTTPException(status_code=404, detail="Could not delete the short url.")   