from fastapi import FastAPI, Request, Response, BackgroundTasks
from fastapi import HTTPException
from contextlib import asynccontextmanager

from pydantic import BaseModel

from typing import Union

import uvicorn
import time
import os
from event import EventHandler, EventPack, ChallengeVerification
import json
import asyncio
import threading

from modules.proxy import Proxy
from modules.message import Message
import uuid
from datetime import datetime


class PostRequest(BaseModel):
        challenge: str
        token: str
        type: str

class ResponseResult(BaseModel):
    challenge: str

class FeishuProxy(Proxy):
    def __init__(self, name, profession='LLM'):
        super().__init__(name, profession)
        #self.message_loop_thread = threading.Thread(target=self.message_loop)
        self.feishu_event = {}
    
    async def send_office(self,content):
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
    
    
    async def receive_office(self,message:Message):
        print(f'receive message from office: {message.content}')
        pass
    
    async def launch(self):
        await self.messenger.arun()
        pass
    
    
    async def event_chat(self,event:EventPack):
        message = await self.send_office(event.event.message.content)
        self.feishu_event[message.id] = {'office_message':message,'app_event':event}
        
        return
    
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    await proxy.launch()
    print(f'life span lanched')
    yield

app = FastAPI(lifespan=lifespan)
#app = FastAPI()
print('Fastapi init')


# @app.on_event("startup")



@app.post("/reach/chat")
async def reach_chat(request: Request , event: Union[ChallengeVerification, EventPack],background_tasks: BackgroundTasks):
    if isinstance(event,ChallengeVerification):
        print(f"event is ChallengeVerification : {event.challenge}")
        await proxy.send_office(event.challenge)
        return ResponseResult(challenge=event.challenge)
    elif isinstance(event, EventPack):
        print(f'schema: {event.schema_v}')
        print(f'event type: {event.header.event_type}')
        # await event_handler.dispatch(event)
        #background_tasks.add_task(event_handler.dispatch,event)
        await proxy.event_chat(event=event)
    else:
        print("impossible event")

    # print(json.dumps(event,indent=2))
    
    return {}


def main():
    print('Feishu Proxy start')
    uvicorn.run(app, host="0.0.0.0", port=8270)
    return

# async def amain():
#     await asyncio.gather(
#         uvicorn.run(app, host="0.0.0.0", port=8270),
#         proxy.launch()
#     )

if __name__ == "__main__":
    # asyncio.run(amain())
    main()