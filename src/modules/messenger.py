import os
from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka import KafkaConsumer
from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
import asyncio
import json
import uuid
import requests
from datetime import datetime
import time
from modules.message import Message,RegisterLancerRequest, RegisterLancerResponse
from modules.utils import custom_value_serializer
class Messenger:
    def __init__(self,agent_id,group_id,async_mode = False):
        # 初始化kafka
        load_dotenv('.env_msg')
        self.async_mode = async_mode
        self.kafka_address =  os.getenv('KAFKA_ADDRESS')
        self.lancer_office_address = os.getenv('LANCER_OFFICE')
        self.group_id = group_id
        
        self.post_address = ""
        self.office_id = ""
        self.agent_id = agent_id
        self.message_cb = None
        
        if self.async_mode:
            #self.consumer_task = asyncio.ensure_future(self.create_async_kafka(group_id))
            pass
        else:
            print(f'Create sync kafka')
            self.kafka_producer = KafkaProducer(bootstrap_servers=self.kafka_address,
                            value_serializer=custom_value_serializer)
                        
            self.kafka_consumer = KafkaConsumer(
                bootstrap_servers=self.kafka_address,
                auto_offset_reset = 'earliest',
                enable_auto_commit=False,
                group_id = group_id
            )
        
        # asyncio.run ok
        # self.consumer_task = asyncio.run(self.create_async_consumer(group_id)) 
        
        
    
    async def create_async_kafka(self,group_id,loop = None):
        print(f'create async consumer event_loopid {id(loop)} running loop id {id(asyncio.get_running_loop())}')
        self.akafka_consumer = AIOKafkaConsumer(
            bootstrap_servers=self.kafka_address,
            auto_offset_reset = 'earliest',
            enable_auto_commit=False,
            group_id = group_id,
            loop=loop
        )
        
        if self.office_id != '' and self.office_id != '-1':
            self.akafka_consumer.subscribe(topics=[self.office_id],listener=None)
        
        self.akafka_producer = AIOKafkaProducer(bootstrap_servers=self.kafka_address,
                            value_serializer=custom_value_serializer,loop=loop)
        await self.akafka_producer.start()

    def post_message(self,receive_id, content):
        # 发送消息
        message = Message(
            id = str(uuid.uuid4()),
            meta_info='',
            content=content,
            sender_id=self.office_id,
            receive_ids=[receive_id],
            create_timestamp=datetime.now()
        )
        
        message_str = message.model_dump_json()
        
        print(f"{datetime.now()} #send to {self.post_address} : {message_str}")
        self.kafka_producer.send(
            self.post_address,
            #dict(message)
            value=message_str
        )
        self.kafka_producer.flush()
                
        return
    async def apost_message(self,receive_id, content):
        if isinstance(content,str):
            message = Message(
                id = str(uuid.uuid4()),
                meta_info='',
                content=content,
                sender_id=self.office_id,
                receive_ids=[receive_id],
                create_timestamp=datetime.now()
            )
        elif isinstance(content,Message):
            message = content
        
        message_str = message.model_dump_json()
        
        print(f"{datetime.now()} #send to {self.post_address} : {message_str}")
        await self.akafka_producer.send_and_wait(
            self.post_address,
            #dict(message)
            value=message_str
        )
        print(f'send over')
        await self.akafka_producer.flush()

    def register(self, lancer_request:RegisterLancerRequest, message_cb=None):
        # 注册消息处理函数        
        if message_cb:
            self.message_cb = message_cb
        
        #通过名字注册一个ID            
        response = requests.post(f'{self.lancer_office_address}/lancer',json = lancer_request.model_dump())
        if response.status_code != 200:
            print('Register to office failed')
            return -1
        
        lancer_response = RegisterLancerResponse(**response.json())

        self.post_address = lancer_response.post_address
        self.office_id = lancer_response.office_id
        
        print(f'{datetime.utcnow()} #self.post_address:{self.post_address}, self.office_id:{self.office_id}')
        
        
        if self.async_mode:
            # asyncio.get_event_loop().run_until_complete(
            #     self.akafka_consumer.subscribe(topics=[self.office_id],listener=None)        
            # )
            # self.akafka_consumer.subscribe(topics=[self.office_id],listener=None)  
            # self.akafka_consumer.subscribe(topics=[self.office_id],listener=None)      
            pass
        else:
            self.kafka_consumer.subscribe(topics=[self.office_id],listener=None)

        return lancer_response.office_id
    
    def unregister(self,topic):
        return
    
    async def aconsumer_kafka_message(self):
        print(f'consumer message begin')
        try:
            async for msg in self.akafka_consumer:
                message = Message.model_validate_json(msg.value.decode('utf-8'))
                print(f'arun: {message}')
                await self.message_cb(message)
                await self.akafka_consumer.commit()
        finally:
            await self.akafka_consumer.stop()

    async def arun(self,loop=None):
        #async def consume_message(self):
        print(f'arun start ,current loop {id(loop)},{id(asyncio.get_event_loop())}')
        if not loop:
            loop = asyncio.get_event_loop()
        await self.create_async_kafka(loop)
        print(f'create_async_kafka ok ')
        await self.akafka_consumer.start()
        print(f'akafka_consumer.start ok ')
        
        asyncio.create_task(self.aconsumer_kafka_message())
        print(f'aconsumer_kafka_message task create')
        return
        try:
            async for msg in self.akafka_consumer:
                message = Message.model_validate_json(msg.value.decode('utf-8'))
                print(f'arun: {message}')
                await self.message_cb(message)
                await self.akafka_consumer.commit()
        finally:
            await self.akafka_consumer.stop()
                    
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(consume_message)
        return
    
    def run(self,sync_run:bool = True):
        if sync_run:
            # 启动Messenger
            for msg in self.kafka_consumer:

                #message_dict = eval(msg.value.decode('utf-8'))
                # message = Message(**message_dict)
                #print(f'run:{msg}')
                # self.kafka_consumer.commit()
                # continue

                message = Message.model_validate_json(msg.value.decode('utf-8'))
                
                self.message_cb(message)
                self.kafka_consumer.commit()
        else:
            async def async_run():
                await self.akafka_consumer.start()
                try:
                    async for msg in self.akafka_consumer:
                        # await self.akafka_consumer.commit()
                        # continue
                    
                        message = Message.model_validate_json(msg.value.decode('utf-8'))
                        print(f'arun: {message}')
                        await self.message_cb(message)
                        await self.akafka_consumer.commit()
                finally:
                    await self.akafka_consumer.stop()
            asyncio.get_event_loop().run_until_complete(async_run())
        return
    
    

def test_messenger():
    messenger = Messenger('1','1')
    asyncio.get_event_loop().run_until_complete(messenger.arun())
    pass

if __name__ == "__main__":
    test_messenger()