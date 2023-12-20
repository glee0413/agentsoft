from typing import List, Optional,Union
from pydantic import BaseModel, Field
import json
from api import MessageApiClient
from pydantic_settings import BaseSettings
import time
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

class EventHandler():
    def __init__(self) -> None:
        self.message_record = MessageRecord()
        pass
    
    async def dispatch(self, event_box: EventPack):
        # print(f'header:event_type:{event_box.header.event_type}, eventid:{event_box.header.event_id}')
        # print(f'event: {event_box.event.sender.sender_id}_{event_box.event.message.chat_type} : {event_box.event.message.content}')
        # print(f"message: {event_box.event.message.message_id}")
        
        #print(event_box)
        
        if self.message_record.message_exist(event_box.event.message.message_id):
            print(f'Message {event_box.event.message.message_id} exist')
            return
        self.message_record.add_message(event_box)
        
        print(event_box.model_dump_json(indent=4))
        time.sleep(10)
        message_api_client.send_text_with_open_id(event_box.event.sender.sender_id.open_id, 
                                                  event_box.event.message.content)
        return
    
test_json="""
    {
    "schema": "2.0",
    "header": {
        "event_id": "5e3702a84e847582be8db7fb73283c02",
        "event_type": "im.message.receive_v1",
        "create_time": "1608725989000",
        "token": "rvaYgkND1GOiu5MM0E1rncYC6PLtF7JV",
        "app_id": "cli_9f5343c580712544",
        "tenant_key": "2ca1d211f64f6438"
    },
    "event": {
        "sender": {
            "sender_id": {
                "union_id": "on_8ed6aa67826108097d9ee143816345",
                "user_id": "e33ggbyz",
                "open_id": "ou_84aad35d084aa403a838cf73ee18467"
            },
            "sender_type": "user",
            "tenant_key": "736588c9260f175e"
        },
        "message": {
            "message_id": "om_5ce6d572455d361153b7cb51da133945",
            "root_id": "om_5ce6d572455d361153b7cb5xxfsdfsdfdsf",
            "parent_id": "om_5ce6d572455d361153b7cb5xxfsdfsdfdsf",
            "create_time": "1609073151345",
            "update_time": "1687343654666",
            "chat_id": "oc_5ce6d572455d361153b7xx51da133945",
            "chat_type": "group",
            "message_type": "text",
            "content": "{\"text\":\"@_user_1 hello\"}",
            "mentions": [
                {
                    "key": "@_user_1",
                    "id": {
                        "union_id": "on_8ed6aa67826108097d9ee143816345",
                        "user_id": "e33ggbyz",
                        "open_id": "ou_84aad35d084aa403a838cf73ee18467"
                    },
                    "name": "Tom",
                    "tenant_key": "736588c9260f175e"
                }
            ],
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.53 Safari/537.36 Lark/6.7.5 LarkLocale/en_US ttnet SDK-Version/6.7.8"
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