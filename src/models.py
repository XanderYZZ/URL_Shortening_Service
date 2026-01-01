from pydantic import AwareDatetime, BaseModel
from typing import Optional

class ShortenedURL(BaseModel):
    url: str
    short_url: str 
    created_at: Optional[AwareDatetime] = None
    updated_at: Optional[AwareDatetime] = None
    access_count: int

class UpdateURLRequest(BaseModel):
    url: str