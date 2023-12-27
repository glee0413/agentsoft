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
class RegisterLancerRequest(BaseModel):
    profession: str
    name: str
    id: str
    assign_type: str #auto自动分配，pm指定
    

class RegisterLancerResponse(BaseModel):
    status: str
    id: str
    keepalive: int

class DeleteLancerResponse(BaseModel):
    status: str
    

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
    
    async def register(self,request:RegisterLancerRequest):
        async with self.lock:
            for lancer in self.bank:
                if lancer.id == request.id:
                    return RegisterLancerResponse(status = 'Failed',id = '-1',keepalive = -1)
                
            new_lancer = FreelancerInfo(profession = request.profession,
                name = request.name, id = request.id,register_time=datetime.now())
            
            new_lancer.office_id = str(uuid.uuid4())
            
            self.bank.append(new_lancer)
        
        return RegisterLancerResponse(status = 'OK',id = new_lancer.office_id,keepalive = 60)
    
    async def delete_lancer(self, office_id: str):
        async with self.lock:
            for lancer in self.bank:
                if lancer.office_id == office_id:
                    self.bank.remove(lancer)
                    return DeleteLancerResponse(status='OK')
        
        return DeleteLancerResponse(status='Failed')

        
    
    def get_profession(profession):
        return

class FreelancerOffice:
    def __init__(self):
        self.lancer_bank = FreelancerBank()

    def register_receiver(self, receiver_id):
        # 注册接收消息的函数
        pass
    
    async def register(self,request:RegisterLancerRequest):        
        return await self.lancer_bank.register(request)
    
    async def delete_lancer(self,office_id : str):
        print(f'delete_lancer: {office_id}')
        return await self.lancer_bank.delete_lancer(office_id)
    
    async def list(self):
        return self.lancer_bank.bank

freelancer_office = FreelancerOffice()

@app.post("/lancer")
async def register_lancer(request:RegisterLancerRequest):
    response =  await freelancer_office.register(request)
    return response

@app.get("/lancer")
async def list_lancer():
    response = await freelancer_office.list()
    return response

@app.delete('/lancer/{office_id}')
async def delete_lancer(office_id: str):
    response = await freelancer_office.delete_lancer(office_id)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8268)