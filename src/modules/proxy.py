from abc import ABC, abstractmethod
from .message import Message,RegisterLancerRequest
from .messenger import Messenger

class Proxy(ABC):
    """
    使用异步的方式来连接外部应用(飞书、微信)与内部agent系统
    外部使用http方式，内部使用kafka
    
    """
    def __init__(self, name, profession='common',group_id = 'Proxy'):
        self.name = name
        self.profession = profession #通过profession来连接对应的profession的agent
        self.group_id = group_id
        self.messenger = Messenger(agent_id=self.name,group_id=self.group_id,async_mode = True)
        lancer_request = RegisterLancerRequest(
            profession = self.profession,
            name = self.name,
            id = self.name,
            assign_type='auto',
            type='proxy',
        )
        
        self.office_id = self.messenger.register(lancer_request = lancer_request,
            message_cb = self.receive_office_message)
        
    
    @abstractmethod
    async def send_office_message(self,content):
        pass
    
    @abstractmethod
    async def receive_office_message(self,message:Message):
        print(message.model_dump_json())
        pass
    
    # @abstractmethod
    # async def send_app(self,content):
    #     pass
    
    # @abstractmethod
    # async def receive_app(self):
    #     pass
    
    @abstractmethod
    def launch(self):
        pass