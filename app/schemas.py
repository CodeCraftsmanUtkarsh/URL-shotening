from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
class URLRequest(BaseModel):
    url: HttpUrl
    custom_code: Optional[str] = None
    expires_in: int = Field(default=30, gt=0)
class URLResponse(BaseModel):
    short_code: str
    original_url: HttpUrl
class ErrorResponse(BaseModel):
    detail: str
class HealthResponse(BaseModel):
    status: str