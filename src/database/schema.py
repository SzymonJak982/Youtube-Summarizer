from typing import List, Union

from pydantic import BaseModel


class Item(BaseModel):
    video_title: str
    timestamp: str
    video_url: str
    summary: str
    method_used: str

    class Config:
        from_attributes = True

