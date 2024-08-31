from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CharacterProfileResponse(BaseModel):
    name: str
    realm: str
    region: str

    # class_name: str
    # current_spec: str

    item_level: int
    last_crawled_at: datetime = Field(default=datetime.now())
