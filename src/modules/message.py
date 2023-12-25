import datetime
from pydantic import BaseModel
from typing import List


class Message(BaseModel):
    id: str
    meta_info: str
    content: str
    sender_id: str
    receive_ids: List[str]
        
class Topic:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.create_time = datetime.now()
        self.participant_ids = []
        self.transcript = []
        self.status = ""