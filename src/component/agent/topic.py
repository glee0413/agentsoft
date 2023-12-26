# TopicBase.py

import hashlib
import time

class TopicBase:
    def __init__(self, sender, receiver):
        self.task_id = hashlib.md5(str(time.time()).encode()).hexdigest()
        self.topic_id = hashlib.md5(str(time.time()).encode()).hexdigest()
        self.topic_name = f"Topic_{self.topic_id}"
        self.sender = sender
        self.receiver = receiver
        self.timestamp = time.time()
        self.message_body = None
        self.response = None

    def fill_message(self, message_body):
        """
        填写消息
        TopicBase消息主要用户agent之间进行传递消息，与大模型的通讯需使用特定模型的api的数据结构
        """
        self.message_body = message_body
