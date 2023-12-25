import os
from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import uuid

from message import Message

class Messenger:
    def __init__(self,sender_id):
        # 初始化kafka
        load_dotenv('.env_msg')
        self.kafka_address =  os.getenv('KAFKA_ADDRESS')
        
        self.kafka_producer = KafkaProducer(bootstrap_servers=self.kafka_address,
                         value_serializer=lambda m: json.dumps(m).encode())
        
        
        
        self.post_offices = []
        self.sender_id = sender_id
        self.message_cb = {}

    def post_message(self,receive_id, content):
        # 发送消息
        message = Message(
            id = str(uuid.uuid4()),
            meta_info='',
            content=content,
            sender_id=self.sender_id,
            receive_ids=[receive_id]
        )
        
        kafka_topic = os.getenv('COMMON_TOPIC')
        print(f'kafka topic {kafka_topic}')
        
        print(f"send message {content}")
        self.kafka_producer.send(
            os.getenv('COMMON_TOPIC'),
            dict(message)
        )
        self.kafka_producer.flush()
        
        print(f"send message {content} over")
        
        return

    def register(self, group_id=None, topic_id = 0, agent_id=None, message_cb=None):
        # 注册消息处理函数
        
        # kafka_topic = topic_id
        kafka_topic = os.getenv('COMMON_TOPIC')
        
        self.kafka_consumer = KafkaConsumer(
            kafka_topic,
            bootstrap_servers=self.kafka_address,
            auto_offset_reset = 'earliest',
            enable_auto_commit=False,
            group_id = 'AI_Agent'
        )
        
        self.message_cb[agent_id] = message_cb
        
        pass

    def run(self):
        # 启动Messenger
        for msg in self.kafka_consumer:
            print(f'Receive message {msg}')
            message_dict = eval(msg.value.decode('utf-8'))
            message = Message(**message_dict)
            print(self.message_cb)
            
            self.message_cb[message.receive_ids[0]](message)
            self.kafka_consumer.commit()
        return
    
    
