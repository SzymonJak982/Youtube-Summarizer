# from typing import List, Union

from pydantic import BaseModel
from typing import Optional

#TODO: Add video ID
class Item(BaseModel):
    video_title: str
    timestamp: str
    video_url: str
    video_id: Optional[str] = None
    summary: str
    method_used: str

    class Config:
        from_attributes = True


class ItemUpdate(Item):
    # TODO:
    pass


