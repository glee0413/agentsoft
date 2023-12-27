import os
from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import uuid
import requests
from datetime import datetime

from message import Message,RegisterLancerRequest, RegisterLancerResponse
from utils import custom_value_serializer
class Messenger:
    def __init__(self,agent_id,group_id):
        # 初始化kafka
        load_dotenv('.env_msg')
        self.kafka_address =  os.getenv('KAFKA_ADDRESS')
        self.lancer_office_address = os.getenv('LANCER_OFFICE')
        
        self.kafka_producer = KafkaProducer(bootstrap_servers=self.kafka_address,
                        value_serializer=custom_value_serializer)
                        #value_serializer=str.encode)
                         #value_serializer=lambda m: json.dumps(m).encode())
        
        # kafka_topic = os.getenv('COMMON_TOPIC')
        
        self.kafka_consumer = KafkaConsumer(
            bootstrap_servers=self.kafka_address,
            auto_offset_reset = 'earliest',
            enable_auto_commit=False,
            group_id = group_id
        )
        
        self.post_address = ""
        self.office_id = ""
        self.agent_id = agent_id
        self.message_cb = None

    def post_message(self,receive_id, content):
        # 发送消息
        message = Message(
            id = str(uuid.uuid4()),
            meta_info='',
            content=content,
            sender_id=self.office_id,
            receive_ids=[receive_id],
            create_timestamp=datetime.utcnow()
        )
        
        # json_str = message.model_dump()
        # print(json_str)
        # message_temp = Message(**json_str)
        message_str = message.model_dump_json()
        
        print(f"{datetime.utcnow()} #send to {self.post_address} : {message_str}")
        self.kafka_producer.send(
            self.post_address,
            #dict(message)
            value=message_str
        )
        self.kafka_producer.flush()
        
        print(f"{datetime.utcnow()} #send message {content} over")
        
        return

    def register(self, lancer_request:RegisterLancerRequest, message_cb=None):
        # 注册消息处理函数        
        if message_cb:
            self.message_cb = message_cb
        
      
        #通过名字注册一个ID            
        response = requests.post(f'{self.lancer_office_address}/lancer',json = lancer_request.model_dump())
        if response.status_code != 200:
            return -1
        
        lancer_response = RegisterLancerResponse(**response.json())

        self.post_address = lancer_response.post_address
        self.office_id = lancer_response.office_id
        
        print(f'{datetime.utcnow()} #self.post_address:{self.post_address}, self.office_id:{self.office_id}')
        
        self.kafka_consumer.subscribe(topics=[self.office_id],listener=None)

        return lancer_response.office_id
    
    def unregister(self,topic):
        return

    def run(self):
        # 启动Messenger
        for msg in self.kafka_consumer:

            #message_dict = eval(msg.value.decode('utf-8'))
            # message = Message(**message_dict)
            print(f'run:{msg}')
            # self.kafka_consumer.commit()
            # continue

            message = Message.model_validate_json(msg.value.decode('utf-8'))
            
            self.message_cb(message)
            self.kafka_consumer.commit()
        return
    
    
