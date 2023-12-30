from datetime import datetime
from pydantic import BaseModel,Field
from typing import List,Optional
import uuid
from datetime import datetime
class Message(BaseModel):
    id: str
    refer_id:Optional[str] = ""
    meta_info: str
    content: str
    sender_id: str
    team_id:Optional[str] = None
    receive_ids: List[str] # 
    create_timestamp:  datetime
    
    #@staticmethod
    def genereat_reply(self):
        reply = Message(
            id = str(uuid.uuid4()),
            refer_id = self.id,
            meta_info='',
            content='',
            sender_id='',
            team_id=self.team_id,
            receive_ids=[self.sender_id],
            create_timestamp=datetime.now())
        return reply
        
    
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
    type:Optional[str] = 'agent' # proxy,agent
    
    

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
    status: Optional[str] = None # ok,offline,die
    register_time: datetime = Field(default_factory=datetime.utcnow)
