# from typing import List, Union

from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    video_title: str
    timestamp: str
    video_url: str
    video_id: Optional[str] = None
    summary: str
    method_used: str

    class Config:
        from_attributes = True


class UpdateItem(Item):
    # regular id not that useful in Youtube context. #TODO: Delete if unnecessary
    id: int


