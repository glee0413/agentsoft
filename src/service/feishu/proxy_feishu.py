from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi import HTTPException
from contextlib import asynccontextmanager

from pydantic import BaseModel

from typing import Union

import uvicorn

import os
from event import EventHandler, EventPack, ChallengeVerification, test_json
import json
import asyncio
import threading

from modules.proxy import Proxy
from modules.message import Message
import uuid
from datetime import datetime
from loguru import logger

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

class FeishuProxy(Proxy):
    def __init__(self, name, profession='LLM'):
        super().__init__(name, profession)
        self.feishu_event = []
        self.event_hander = EventHandler()
        
        # event_dict = json.loads(test_json)
        # self.test_event = EventPack(**event_dict)
        pass
        
    async def send_office_message(self,content):
        message = Message(
                id = str(uuid.uuid4()),
                refer_id='',
                meta_info='',
                content=content,
                sender_id=self.office_id,
                receive_ids=[self.profession],
                create_timestamp=datetime.now()
            )
        
        await self.messenger.apost_message(receive_id = self.profession, content = message)
        return message
    
    
    async def receive_office_message(self,message:Message):
        logger.info(f'receive message from office: {message.content}')
        #TODO: 发送给飞书
        await self.reply_feishu(message=message)
        pass
    
    async def launch(self):
        await self.messenger.arun()
        pass
    
    
    ### 处理与飞书的逻辑
    
    async def reply_feishu(self,message:Message):
        event = None
        for ev in self.feishu_event:
            if message.refer_id == ev['office_message'].id:
                event = ev
                break
            
        if not event:
            logger.error(f'Unknonw message {message}')
            return
        
        self.event_hander.areply(event_box=event,reply_content=message.content)
        return
    
    async def event_chat(self,event:EventPack):
        message = await self.send_office_message(event.event.message.content)
        #self.feishu_event[message.id] = {'office_message':message,'app_event':event}
        self.feishu_event.append({'office_message':message,'app_event':event})
        
        return
    
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

proxy = FeishuProxy('Feishu',profession='LLM')
logger.info('FeishuProxy init ok')

@asynccontextmanager
async def lifespan(app: FastAPI):
    await proxy.launch()
    logger.info(f'Fastapi lifespace start')
    yield

app = FastAPI(lifespan=lifespan)
#app = FastAPI()
logger.info('Fastapi init')


# @app.on_event("startup")



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
    main()