from agent import LLMAgent
from message import Message
from langchain.prompts import ChatPromptTemplate
from prompt.dev_prompt import python_coder_template


class CoderAgent(LLMAgent):
    def __init__(self, name):
        super().__init__(name)
        self.python_hat = ChatPromptTemplate.from_template(python_coder_template)
        
        
    def ReceiveMessage(self,message:Message):
        return
    
    def PostMessage(self,content):
        return
    
    def Conclude(self):
        # 总结的函数
        pass
    
    def launch(self):
        return
    
    def stop(self):
        return
    
    def stop(self):
        # 停止Agent
        pass

def test_llmagent():
    LLMAgent('LLMAgent')
    pass

if __name__ == "__main__":
    test_llmagent()