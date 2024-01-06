from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi import HTTPException
from contextlib import asynccontextmanager

from pydantic import BaseModel

from typing import Union

import uvicorn

import os
from event import EventHandler, EventPack, ChallengeVerification, test_chat_json
import json
import asyncio
import threading

from modules.proxy import Proxy
from modules.message import Message
import uuid
from datetime import datetime
from loguru import logger
from config.constant import ProfessionType
from api import MessageApiClient
from config import constant

class PostRequest(BaseModel):
        challenge: str
        token: str
        type: str

class ResponseResult(BaseModel):
    challenge: str
    
class MessageRecord(BaseModel):
    role: str
    message: Message
    event:EventPack

class FeishuRobotAccount(BaseModel):
    app_id: str
    app_secret: str
    verification_token: str
    encrypt_key: str
    lark_host: str

class FeishuProxy(Proxy):
    def __init__(self, name, profession=ProfessionType.PT_LLM.value):
        super().__init__(name, profession)
        #TODO: 需要用redis来记录聊天记录
        self.feishu_event = {}
        self.event_hander = EventHandler()
        
        event_dict = json.loads(test_chat_json)
        self.test_event = EventPack(**event_dict)
        self.robot_account = {}
        self.message_client = {}
        self.load_robot_config('feishu.json')
        logger.debug(self.robot_account)
        # self.message_client = MessageApiClient()
        

    def load_robot_config(self,config_file):
        with open(config_file,'r') as f:
            data = json.load(f)
            for key in data.keys():
                self.robot_account[key] = FeishuRobotAccount(**data[key])
                # message_api_client = MessageApiClient(env_config.APP_ID, env_config.APP_SECRET, env_config.LARK_HOST)

                self.message_client[key] = MessageApiClient(self.robot_account[key].app_id,
                                                            self.robot_account[key].app_secret,
                                                            self.robot_account[key].lark_host)
                
        
    async def send_office_message(self,content,profession = ProfessionType.PT_LLM.value):
        message = Message(
                id = str(uuid.uuid4()),
                refer_id='',
                meta_info='',
                content=content,
                sender_id=self.office_id,
                receive_ids=[self.profession],
                profession=profession,
                create_timestamp=datetime.now()
            )
        
        await self.messenger.apost_message(receive_id = self.profession, content = message)
        return message
    
    
    async def receive_office_message(self,message:Message):
        logger.info(f'receive message from office: {message.content}')
        #TODO: 发送给飞书
        await self.reply_feishu(message=message)
        
    
    async def launch(self):
        await self.messenger.arun()
        pass
    
    
    ### 处理与飞书的逻辑
    
    async def reply_feishu(self,message:Message):
        event = None
        profession = message.profession
        if not any( profession == item.value[0] for item in ProfessionType):
            logger.error(f'unknown message profession', message)
            return
        if profession not in self.feishu_event:
            logger.error(f'No {profession} context chat')
            return
        
        for ev in self.feishu_event[profession]:
            if message.refer_id == ev['office_message'].id:
                event = ev['app_event']
                break
            
        if not event:
            logger.error(f'Unknonw message {message}')
            return
        
        await self.event_hander.areply(event_box=event,reply_content=message.content)
        return
    
    async def event_chat(self,event:EventPack,profession=ProfessionType.PT_LLM.value):
        message = await self.send_office_message(event.event.message.content,profession=profession)
        #self.feishu_event[message.id] = {'office_message':message,'app_event':event}
        if profession not in self.feishu_event:
            self.feishu_event[profession] = []
        self.feishu_event[profession].append({'office_message':message,'app_event':event})
        
        return {}
    
    async def chat_history(self):
        return self.feishu_event
    
    # @app.post("/event_notifier")
    # async def event_notifier(request: Request , event: Union[ChallengeVerification, EventPack],background_tasks: BackgroundTasks):
    #     if isinstance(event,ChallengeVerification):
    #         print(f"event is ChallengeVerification : {event.challenge}")

    #         return ResponseResult(challenge=event.challenge)
    #     elif isinstance(event, EventPack):
    #         print(f'schema: {event.schema_v}')
    #         print(f'event type: {event.header.event_type}')
    #         # await event_handler.dispatch(event)
    #         # background_tasks.add_task(event_handler.dispatch,event)
    #         #TODO: 接收处理函数
    #     else:
    #         print("impossible event")

    #     # print(json.dumps(event,indent=2))
        
    #     return {}

proxy = FeishuProxy('Feishu Proxy')
logger.info('Feishu Proxy init ok')

# proxy_python = FeishuProxy('Python_expert',profession='LLM_Python')
# logger.info('Python expert init ok')

@asynccontextmanager
async def lifespan(app: FastAPI):
    await proxy.launch()
    logger.info(f'Fastapi lifespace start')
    yield

#app = FastAPI()
app = FastAPI(lifespan=lifespan)
logger.info('Fastapi init')


@app.post("/reach/chat")
async def reach_chat(request: Request , event: Union[ChallengeVerification, EventPack],background_tasks: BackgroundTasks):
    if isinstance(event,ChallengeVerification):
        logger.debug(f"event is ChallengeVerification : {event.challenge}")
        await proxy.send_office_message(event.challenge)
        #proxy.test_event.event.message.content = event.challenge
        #await proxy.event_chat(event=proxy.test_event)
        return ResponseResult(challenge=event.challenge)
    elif isinstance(event, EventPack):
        logger.debug(f'schema: {event.schema_v}')
        logger.debug(f'event type: {event.header.event_type}')
        # await event_handler.dispatch(event)
        #background_tasks.add_task(event_handler.dispatch,event)
        await proxy.event_chat(event=event)
    else:
        logger.error("impossible event type")

    # print(json.dumps(event,indent=2))
    return {}

async def feishu_interface(request: Request , event: Union[ChallengeVerification, EventPack],
                           background_tasks: BackgroundTasks,profession=ProfessionType.PT_LLM.value):
    if isinstance(event,ChallengeVerification):
        logger.debug(f"event is ChallengeVerification : {event.challenge}")
        return ResponseResult(challenge=event.challenge)
    elif isinstance(event, EventPack):
        logger.info(f'#######\n event:\n{event}\n#######')
        # await event_handler.dispatch(event)
        #background_tasks.add_task(event_handler.dispatch,event)
        await proxy.event_chat(event=event,profession=profession)
    else:
        logger.error("impossible event type")

@app.post('/reach/python_expert')
async def reach_python_expert(request: Request,
                              event: Union[ChallengeVerification, EventPack],
                              background_tasks: BackgroundTasks):
    return await feishu_interface(request=request,
                           event=event,background_tasks=background_tasks,
                           profession=ProfessionType.PT_EXPERT_PYTHON.value)
    


@app.get("/proxy/chat_history")
async def proxy_chat_history():
    history = await proxy.chat_history()
    return history

def main():
    logger.info('Feishu Proxy start')
    uvicorn.run(app, host="0.0.0.0", port=8270)
    return

# async def amain():
#     await asyncio.gather(
#         uvicorn.run(app, host="0.0.0.0", port=8270),
#         proxy.launch()
#     )

if __name__ == "__main__":
    # asyncio.run(amain())
    #DEBUG: 暂时关闭文件读写
    #logger.add(sys.stderr, level="INFO")

    #logger.add(os.path.basename(__file__)+'.log',backtrace=True, diagnose=True,rotation="500 MB")
    log_file = os.path.basename(__file__) + '.log'
    logger.add(log_file,backtrace=True, diagnose=True,rotation="500 MB",serialize=True)
    
    main()