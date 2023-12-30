import sys
# print(sys.path)

import uuid
from abc import ABC, abstractmethod

import time
from datetime import datetime
import asyncio
from modules.model_center import ModelCenter
from modules.messenger import Messenger
from modules.message import Message,RegisterLancerRequest, RegisterLancerResponse

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

class Agent(ABC):
    def __init__(self, name, async_mode = False, profession = 'empty'):
        self.id = str(uuid.uuid4())
        self.name = name
        self.async_mode = async_mode
        self.resume = ''
        self.profession = profession
        # team_id: [agent_a_id,agent_b_id]
        self.teammate = {}
        # 相同职能的人，可相互补充完成同类的问题
        self.group_id = ''
        # 不同职能，通过协同合作来达到共同目标
        self.team_id =[]
                
        self.messenger = Messenger(agent_id=self.id,group_id=self.profession,async_mode = self.async_mode)
        lancer_request = RegisterLancerRequest(
            profession = self.profession,
            name = self.name,
            id = self.id,
            assign_type='auto'
        )
        self.office_id = self.messenger.register(lancer_request = lancer_request,
            message_cb = self.ReceiveMessage)
        
    @abstractmethod
    def ReceiveMessage(self,message:Message):
        pass
    
    @abstractmethod
    def PostMessage(self,receive_id,content):
        pass
    
    @abstractmethod
    def Conclude(self):
        # 总结的函数
        pass
    
    @abstractmethod
    def launch(self):
        # 启动Agent
        pass
    
    @abstractmethod
    def stop(self):
        # 停止Agent
        pass

class EchoAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
    
    # 如使用异步方式，在lanch函数里面要用调用异步run方式
    async def ReceiveMessage(self, message: Message):
        # 接收消息的函数
        print(f"{datetime.now()}#: {message.content}")
        
        await asyncio.sleep(1) 
        #time.sleep(1)
        await self.aPostMessage(content = message.content)
        
    
    async def aPostMessage(self, receive_id:str='all',content : str = ''):
        await self.messenger.apost_message(receive_id = receive_id, content = content)
    
    def PostMessage(self, receive_id:str='all',content : str = ''):
        self.messenger.post_message(receive_id = receive_id, content = content)
    
    def Conclude(self):
        # 总结的函数
        pass
    
    def launch(self):
        # 启动Agent
        # self.messenger.run()
        # self.messenger.arun()
        # asyncio.get_event_loop().run_until_complete(self.messenger.arun())
        print(f'launched')
        self.messenger.run(sync_run=False)
    
    def stop(self):
        # 停止Agent
        pass

class LLMAgent(Agent):
    def __init__(self, name):
        super().__init__(name,async_mode=True,profession = 'LLM')
        self.llm = ModelCenter()
        
        asyncio.get_event_loop().run_until_complete(
            self.messenger.create_async_kafka(asyncio.get_event_loop())
        )
        
    # 负责调用外部大模型
    async def ReceiveMessage(self,message:Message):
        print(f"{datetime.now()}#: {message.content}")
        answer = await self.Conclude(message.content)
        
        # reply = Message(
        #         id = str(uuid.uuid4()),
        #         meta_info='',
        #         content=answer,
        #         sender_id=self.office_id,
        #         receive_ids=[message.sender_id],
        #         refer_id=message.id,
        #         create_timestamp=datetime.now()
        #     )
        reply = message.genereat_reply()
        reply.content = answer
        
        await self.PostMessage(message.sender_id,reply)
        return
    
    async def PostMessage(self,receive_id:str='all',content : str = ''):
        await self.messenger.apost_message(receive_id = receive_id, content = content)
        return
    
    async def Conclude(self,content):
        # 总结的函数
        answer = await self.llm.aask(content)
        return answer
    
    def launch(self):
        self.messenger.run(sync_run=False)
        return
    
    def stop(self):
        return
    
    

class RLLMAgent():
    # 负责调用本地大模型
    pass



def test_agent():
    agent = EchoAgent('小睿慧聊')
    agent.PostMessage(content = 'echo')
    
    agent = LLMAgent('小睿大模')
    #agent.PostMessage(content = 'echo')
    asyncio.get_event_loop().run_until_complete(agent.PostMessage(content='echo'))
    
    # asyncio.get_event_loop().run_until_complete(agent.PostMessage(content='echo'))
    # agent.launch()
    

if __name__ == "__main__":
    test_agent()