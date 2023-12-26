from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime
import uuid
import asyncio
import uvicorn

app = FastAPI()

# 向postman注册简历
class RegisterRequest(BaseModel):
    profession: str
    name: str
    id: str
    assign_type: str #auto自动分配，pm指定
    

class RegisterResponse(BaseModel):
    status: str
    id: str
    keepalive: int
    

class FreelancerInfo(BaseModel):
    profession: str
    name: str
    id: str
    office_id: Optional[str] = None
    team_id: Optional[List[str]] = None
    group_id: Optional[List[str]]  = None
    status: Optional[str] = None
    register_time: datetime
    

class FreelancerBank():
    def __init__(self) -> None:
        self.bank = []
        self.teams = []
        self.groups = []
        self.lock = asyncio.Lock()
    
    async def register(self,request:RegisterRequest):
        print('FreelancerBank called')
        async with self.lock:
            print('FreelancerBank lock')
            for lancer in self.bank:
                if lancer.id == request.id:
                    return RegisterResponse(status = 'Failed',id = '-1',keepalive = -1)
                
            new_lancer = FreelancerInfo(profession = request.profession, 
                name = request.name, id = request.id,register_time=datetime.now())
            
            new_lancer.office_id = str(uuid.uuid4())
            
            self.bank.append(new_lancer)
        
        return RegisterResponse(status = 'OK',id = new_lancer.office_id,keepalive = 60)
    
    def get_profession(profession):
        return

class FreelancerOffice:
    def __init__(self):
        self.bank = FreelancerBank()

    def register_receiver(self, receiver_id):
        # 注册接收消息的函数
        pass
    
    async def register(self,request:RegisterRequest):
        print('register called')
        await self.bank.register(request)
        return

freelancer_office = FreelancerOffice()

@app.post("/register")
async def register(request:RegisterRequest):
    
    await freelancer_office.register(request)
    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8268)