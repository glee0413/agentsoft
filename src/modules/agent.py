import sys
# print(sys.path)

from messenger import Messenger
from message import Message
import uuid

class PromptTemplate:
    def __init__(self, template, parameter):
        self.template = template
        self.parameter = parameter

    def show_prompt(self):
        # 根据模板和参数生成提示信息并进行展示
        pass
    
    
class HatRack:
    def __init__(self):
        self.hats = {}

    def show_hats(self):
        # 展示所有帽子的信息
        pass

    def get_hats(self, rolename):
        # 根据角色名获取对应的帽子
        pass

class Agent:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
        self.resume = ''
        self.classmate = []
        
        self.messenger = Messenger(self.id)
        
        self.messenger.register(topic_id = self.id,agent_id = self.id,message_cb = self.ReceiveMessage)
        

    def ReceiveMessage(self,message:Message):
        # 接收消息的函数
        print(message.id)
        print(message.content)
        pass

    def PostMessage(self,content):
        self.messenger.post_message(self.id, content)
        pass

    def Conclude(self):
        # 总结的函数
        pass

    def launch(self):
        # 启动Agent
        self.messenger.run()
        pass

    def stop(self):
        # 停止Agent
        pass
    
class LLMAgent():
    # 负责调用外部大模型
    pass

class RLLMAgent():
    # 负责调用本地大模型
    pass



def test_agent():
    agent = Agent('小睿慧聊')
    agent.PostMessage('hello world')
    agent.launch()
    

if __name__ == "__main__":
    test_agent()