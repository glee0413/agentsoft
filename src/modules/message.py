from datetime import datetime
from pydantic import BaseModel,Field
from typing import List,Optional

class Message(BaseModel):
    id: str
    meta_info: str
    content: str
    sender_id: str
    receive_ids: List[str]
    create_timestamp:  datetime
    
class Topic:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.create_time = datetime.now()
        self.participant_ids = []
        self.transcript = []
        self.status = ""
        
# 向postman注册简历
class RegisterLancerRequest(BaseModel):
    profession: str
    name: str
    id: str
    assign_type: str #auto自动分配，pm指定
    

class RegisterLancerResponse(BaseModel):
    status: str
    office_id: str
    post_address : str
    keepalive: int

class DeleteLancerResponse(BaseModel):
    status: str
    

class FreelancerInfo(BaseModel):
    profession: str
    name: str
    id: str
    office_id: str
    team_id: Optional[List[str]] = None
    group_id: Optional[List[str]]  = None
    status: Optional[str] = None
    register_time: datetime = Field(default_factory=datetime.utcnow)
