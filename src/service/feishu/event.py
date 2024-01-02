from typing import List, Optional,Union
from pydantic import BaseModel, Field
import json
from api import MessageApiClient
from pydantic_settings import BaseSettings
import time
import asyncio
import concurrent.futures
from loguru import logger
class ChallengeVerification(BaseModel):
    challenge: str
    token: str
    type: str

class SenderId(BaseModel):
    union_id: str
    user_id: str
    open_id: str

class Sender(BaseModel):
    sender_id: SenderId
    sender_type: str
    tenant_key: str

class Mention(BaseModel):
    key: str
    id: SenderId
    name: str
    tenant_key: str

class Message(BaseModel):
    message_id: str
    parent_id: Optional[str] = None
    root_id: Optional[str] = None
    create_time: str
    update_time: str
    chat_id: str
    chat_type: str
    message_type: str
    content: str
    mentions: Optional[List[Mention]] = None
    user_agent: Optional[str] = None

class Header(BaseModel):
    event_id: str
    event_type: str
    create_time: str
    token: str
    app_id: str
    tenant_key: str

class Event(BaseModel):
    sender: Sender
    message: Message

class EventPack(BaseModel):
    schema_v: str = Field(..., alias="schema")
    header: Header
    event: Event

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

class MessageRecord():
    def __init__(self) -> None:
        self.message_list = {}
    
    def add_message(self, event_box: EventPack):
        if event_box.event.message.message_id not in self.message_list:
            self.message_list[event_box.event.message.message_id] = event_box
            return True
        return False

    def message_exist(self,message_id):
        if message_id in self.message_list:
            return True
        else:
            return False
    def delete_message(self, message_id):
        self.message_list.pop(message_id)



class EventHandler():
    def __init__(self) -> None:
        self.message_record = MessageRecord()
        self.event_loop = asyncio.get_event_loop()
        # 可通过freelancer进行通知，改变状态
        self.debug = False
        pass
    
    def answer_deeply(self,message_id:str, open_id:str, questen:str):
        time.sleep(10)
        print('answer_deeply awake')
        return 'OK'
    
        message_api_client.send_text_with_open_id(open_id, questen)
        self.message_record.delete_message(message_id)
        return
    
    def dumb_reply(self,openid,content):
        print(f'{openid} : {content}')
    
    async def areply(self,event_box,reply_content):
        
        loop = asyncio.get_event_loop()
        # loop.run_until_complete(
        #     message_api_client.send_text_with_open_id(event_box.event.sender.sender_id.open_id, 
        #                                            event_box.event.message.content)
        # )
        if self.debug:
            # loop.run_until_complete(
            #     self.dumb_reply(event_box.event.sender.sender_id.open_id, 
            #                                         event_box.event.message.content)
            # )
            await loop.run_in_executor(
                    None,self.dumb_reply,
                    event_box.event.sender.sender_id.open_id, 
                    event_box.event.message.content
                )
        else:
            # loop.run_until_complete(
            #     message_api_client.send_text_with_open_id(event_box.event.sender.sender_id.open_id, 
            #                                         event_box.event.message.content)
            # )
            feishu_content = json.dumps({'text':f'{reply_content}'})
            # logger.info(f'message:{reply_content} ,event {event_box.event.message.content}, 
            #             feishu content {feishu_content} ')
            logger.info(f'feishu content:{feishu_content}')
            
            await loop.run_in_executor(
                    None,message_api_client.send_text_with_open_id,
                    event_box.event.sender.sender_id.open_id, 
                    #event_box.event.message.content
                    feishu_content
                )
    
    def dispatch(self, event_box: EventPack):
        # print(f'header:event_type:{event_box.header.event_type}, eventid:{event_box.header.event_id}')
        # print(f'event: {event_box.event.sender.sender_id}_{event_box.event.message.chat_type} : {event_box.event.message.content}')
        # print(f"message: {event_box.event.message.message_id}")
        
        #print(event_box)
        
        # if self.message_record.message_exist(event_box.event.message.message_id):
        #     print(f'Message {event_box.event.message.message_id} exist')
        #     return
        self.message_record.add_message(event_box)
        
        # print(event_box.model_dump_json(indent=4))
        
        print(f'dispatch message:')
        
        # message_api_client.send_text_with_open_id(event_box.event.sender.sender_id.open_id, 
        #                                           event_box.event.message.content)
        
        # loop = asyncio.get_event_loop()
        
        # answer_futrue = loop.run_in_executor(None,self.answer_deeply,
        #                                      event_box.event.message.message_id,
        #                                      event_box.event.sender.sender_id.open_id,
        #                                      event_box.event.message.content
        #                                      )
        
        # await answer_futrue
        
        self.answer_deeply(event_box.event.message.message_id,
                        event_box.event.sender.sender_id.open_id,
                        event_box.event.message.content)
        
        
        return
    
test_chat_json="""
{
  "schema": "2.0",
  "header": {
    "event_id": "0e6fc6b9c4c9047f9d73847732e754d2",
    "event_type": "im.message.receive_v1",
    "create_time": "1704099384553",
    "token": "LUwSr560MJogoqZzoQxbIeMmEkqB44kq",
    "app_id": "cli_a5fd980539ba900e",
    "tenant_key": "1612ab78628e5740"
  },
  "event": {
    "sender": {
      "sender_id": {
        "union_id": "on_a6c9c3010bebb2de2d9080d2387b942d",
        "user_id": "bdbge882",
        "open_id": "ou_75f5f69117065340f0f7a330f4b054fa"
      },
      "sender_type": "user",
      "tenant_key": "1612ab78628e5740"
    },
    "message": {
      "message_id": "om_5404dc52a18c7e0e7666025e6ca90ab5",
      "parent_id": null,
      "root_id": null,
      "create_time": "1704099384316",
      "update_time": "1704099384316",
      "chat_id": "oc_ba1e4e5ae2341aa5656f353df8c29b84",
      "chat_type": "p2p",
      "message_type": "text",
      "content": "{\\"text\\":\\"请写鸡兔同笼的问题python代码\\"}",
      "mentions": null,
      "user_agent": null
    }
  }
}
"""

test_json2="""
{ 
    "challenge": "ajls384kdjx98XX",
    "token": "xxxxxx",
    "type": "url_verification"
}
"""
class User(BaseModel):
    name: str
    age: Optional[int] = None

def main_test():
    
    user = User(name='a')
    
    print(user)
    
    # event_dict = json.loads(test_json)
    # event = EventPack(**event_dict)
    
    
    return

if __name__ == "__main__":
    main_test()