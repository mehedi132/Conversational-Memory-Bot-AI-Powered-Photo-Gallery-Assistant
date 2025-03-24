from pydantic import BaseModel
from typing import List, Optional

class ImageResponse(BaseModel):
    id: str
    src: str
    description: Optional[str]
    tags: Optional[List[str]]

    class Config:
        from_attributes = True