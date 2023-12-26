import uuid


class MessageCenter():
    pass

class AgentBase():
    def __init__(self, config) -> None:
        # 自身属性
        self.http_event_notify = None
        self.memory = None
        self.system_prompt = ""
        self.name = "张三"
        self.uuid = uuid.uuid4
        
        # 社群属性
        
        self.group_list = []
        self.mail_box = None
    
    # 启动工作
    def run():
        return
    
    def die():
        return
    

class AgentFactory():
    """
    AgentFactory 用于生成各种需求的agent
    """
    
    def __init__(self) -> None:
        pass
    
    def create(config):
        """
        根据需求生产不同类型的机器人
        """
        return