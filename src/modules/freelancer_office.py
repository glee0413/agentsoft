from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi import HTTPException

from datetime import datetime
import uuid
import asyncio
import uvicorn
from dotenv import load_dotenv
import os
import json
import threading


from kafka import KafkaProducer,KafkaConsumer
from pydantic import BaseModel
from typing import List,Optional
from utils import custom_value_serializer
from message import Message,RegisterLancerRequest,RegisterLancerResponse,DeleteLancerResponse,FreelancerInfo

app = FastAPI()


class FreelancerBank():
    def __init__(self) -> None:
        self.bank:FreelancerInfo = []
        self.teams = []
        self.groups = []
        self.lock = asyncio.Lock()
        self.agent_idx = 0
        self.proxy_idx = 0
    
    async def register(self,request:RegisterLancerRequest):
        async with self.lock:
            for lancer in self.bank:
                if lancer.id == request.id:
                    print(f'lancer request {request.id} repeat')
                    return '-1'
            # office_id = f'office.{str(uuid.uuid4())}'
            # office_test_id = 'lancer.123'
            if request.type == 'agent':
                office_id = f'{request.type}.{request.profession}.{self.agent_idx}'
                self.agent_idx += 1
            elif request.type == 'proxy':
                office_id = f'{request.type}.{request.profession}.{self.proxy_idx}'
                self.proxy_idx += 1
            else:
                print(f'Invalid type {request.type}')
                return '-1'
            
            new_lancer = FreelancerInfo(profession = request.profession,
                name = request.name,office_id = office_id, 
                id = request.id,register_time=datetime.utcnow())
                        
            self.bank.append(new_lancer)
        return new_lancer.office_id
        # return RegisterLancerResponse(status = 'OK',office_id = new_lancer.office_id,keepalive = 60)
    
    async def delete_lancer(self, office_id: str):
        async with self.lock:
            for lancer in self.bank:
                if lancer.office_id == office_id:
                    self.bank.remove(lancer)
                    return DeleteLancerResponse(status='OK')
        
        return DeleteLancerResponse(status='Failed')

    def select_lancer_officeids(self, scope):
        lancer_ids = []
        if scope == 'all':
            for lancer in self.bank:
                if lancer.status != 'die':
                    lancer_ids.append(lancer.office_id)
        else:
            print(f'scope:{scope} type: {type(scope)}')
            lancer_ids.append(scope)
        return lancer_ids
    
    def get_profession(profession):
        return

class FreelancerOffice:
    def __init__(self,name='FreelancerOffice'):
        load_dotenv('.env_msg')
        self.kafka_address =  os.getenv('KAFKA_ADDRESS')
        self.lancer_bank = FreelancerBank()
        self.post_address = "Freelance.theseus"
        
        self.name = name
        # 固定group_id，防止历史消息被重复消费
        self.group_id = self.name
        
        self.kafka_producer = KafkaProducer(bootstrap_servers=self.kafka_address,
                         value_serializer=custom_value_serializer)
        self.kafka_consumer = KafkaConsumer(
            self.post_address,
            bootstrap_servers=self.kafka_address,
            auto_offset_reset = 'earliest',
            enable_auto_commit=False,
            group_id = self.group_id,
            #consumer_timeout_ms=1000,
        )        
        
        
        self.message_loop_thread = threading.Thread(target=self.message_loop)
        self.thread_stop = False
    
    def post_message(self,receive_id:str,message:Message):
        print(f'{datetime.now()}# send {receive_id}: {message.model_dump_json()}')
        
        office_ids = []
        office_ids = self.lancer_bank.select_lancer_officeids(receive_id)
        
        for oid in office_ids:
            message_str = message.model_dump_json()
            self.kafka_producer.send(oid,message_str)
            self.kafka_producer.flush()
    
    # 逻辑处理类
    #TODO: 消息分为两种：1，自己主动发送的给各个lancer的消息，2代理外部agent的消息，不使用内部的消息格式和通讯机制
    def message_loop(self):
        print(f'message loop start')
        for msg in self.kafka_consumer:
            if self.thread_stop:
                return
            if msg is None:
                #TODO 超时
                print('Timeout')
                continue
            
            msg_ts = datetime.fromtimestamp(msg.timestamp / 1000)
      
            print(f'{datetime.now()}#{datetime.now()-msg_ts}# {msg.value}')

            message = Message.model_validate_json(msg.value.decode('utf-8'))

            if message.content == 'echo':
                self.post_message(receive_id = message.sender_id,message=message)
            
                
            self.kafka_consumer.commit()
        return
    
    def message_process(self,message:Message):
        
        return
    
    def start_message_loop(self,start : bool = True):
        if start:
            self.message_loop_thread.start()
        else:
            self.thread_stop = True
    
    # 接口类
    async def register(self,request:RegisterLancerRequest):        
        office_id = await self.lancer_bank.register(request)
        if office_id == '-1':
            return RegisterLancerResponse(status = 'failed',office_id = office_id,
                                          post_address = self.post_address, keepalive = 60)
        
        return RegisterLancerResponse(status = 'OK',office_id = office_id,
                                          post_address = self.post_address, keepalive = 60)
    
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
    freelancer_office.message_loop_thread.start()
    uvicorn.run(app, host="0.0.0.0", port=8268)