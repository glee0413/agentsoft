from fastapi import FastAPI, Request, Response
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import Union

import uvicorn
import time
import os
from event import EventHandler, EventPack, ChallengeVerification
from api import MessageApiClient
import json

app = FastAPI()


class PostRequest(BaseModel):
    challenge: str
    token: str
    type: str

class ResponseResult(BaseModel):
    challenge: str

class WebStatus():
    def __init__(self) -> None:
        self.ping_count = 0
        self.stage = 'test'
        
web_status = WebStatus()

class FeishuConfig(BaseSettings):
    APP_ID: str
    APP_SECRET: str
    VERIFICATION_TOKEN: str
    ENCRYPT_KEY: str
    LARK_HOST: str
    class Config:
        env_file = ".env_feishu"

env_config = FeishuConfig()

message_api_client = MessageApiClient(env_config.APP_ID, env_config.APP_SECRET, env_config.LARK_HOST)
event_handler = EventHandler()

@app.post("/url_verification")
async def url_verification(request: PostRequest):
    web_status.ping_count += 1
    try:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"{web_status.ping_count}: {request.challenge}")
        if request.type == "url_verification":
            return ResponseResult(challenge=request.challenge)
        else:
            raise HTTPException(status_code=400, detail="Invalid request type")
    except Exception as e:
        print(f"Error processing POST request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Union[ChallengeVerification, EventPack]

@app.post("/event_notifier")
async def event_notifier(request: Request , event: EventPack):
    if isinstance(event,ChallengeVerification):
        print("event is ChallengeVerification")
        return ResponseResult(challenge=event.challenge)
    elif isinstance(event, EventPack):
        print(f'schema: {event.schema_v}')
        print(f'event type: {event.header.event_type}')
        await event_handler.dispatch(event)
    else:
        print("impossible event")

    # print(json.dumps(event,indent=2))
    
    return {}

@app.middleware("http")
async def log_request(request: Request, call_next):
    # 获取访问的URL
    url = str(request.url)
    
    # 记录日志
    print(f"请求的URL: {url}")
    print(f"请求的base_url: {request.base_url}")
    print(f"请求的方法: {request.method}")
    print(f"请求的头部: {request.headers}")
    print(f"请求的查询参数: {request.query_params}")
    print(f"请求的路径参数: {request.path_params}")
    print(f"请求的Cookies: {request.cookies}")
    
    # print(f"请求的主体: {await request.json()}")
    
    # if request.method == 'POST':
    #     print(f"请求的主体: {await request.json()}") 
    
    # 继续处理请求
    response = await call_next(request)
    
    return response


@app.post("/im.message.receive_v1")
def message_receive_event_handler(req_data: dict):
    print(json.dumps(req_data,indent=2))
    # sender_id = req_data.event.sender.sender_id
    # message = req_data.event.message

    # print(f'{sender_id}:{message}')
    
    # if message.message_type != "text":
    #     print("Other types of messages have not been processed yet")
    #     raise HTTPException(status_code=400, detail="Other types of messages have not been processed yet")

    # # get open_id and text_content
    # open_id = sender_id.open_id
    # text_content = message.content

    # # echo text message
    # message_api_client.send_text_with_open_id(open_id, text_content)

    return {}

def main_test_config():
    print(env_config.APP_ID)
    print(env_config.APP_SECRET)
    print(env_config.VERIFICATION_TOKEN)
    print(env_config.ENCRYPT_KEY)
    print(env_config.LARK_HOST)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8264)
