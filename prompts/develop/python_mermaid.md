### System Prompt
你现在是世界知识的专家，擅长用后退的提问策略；请你深呼吸，一步步仔细思考并回答问题。

### User Message

# 软件需求规范:
请根据下面的mermaid的类图生成python代码，Message类是需要发送的消息体，需要pydantic验证
``` mermaid
classDiagram

    class Message{
        +String id
        +String meta_info
        +String content
        +String sender_id
        +List[String] receive_ids
    }

    class Topic{
        +String id
        +String name
        +Datatime create_time
        %% 所有话题的参与者
        +List participant_id 
        %% 按照时序记录消息
        +List[Message] transcript
        +String status
    }

    Topic *-- Message

    class PostOffice{
        +String id
        +String name

        %% 注册一个函数用于处理接收消息
        +MessageCBRegister(receiver_id,)
    }

    %% 消息中间件，封装fastapi和kafka，为postoffic和agent提供消息服务
    class Messenger{
        + PostMessage(Message msg)
        + Register(Group groupId=None, Agent agentId,message_cb)
        + Run()
    }
```

生成格式要求：
代码输出格式为markdown代码段，示例如下：
```python
import os
def main():
    print('hello world')
if __name__ == "__main__":
    main()
```

# 生成代码要求
- 请使用python实现
- 生成代码中只包含必要的包。
- 生成代码需要涵盖函数列表中列出的所有函数。
- 生成代码需要虑到执行性能、内存占用、可用性、可维护性、可扩展性。
- 生成的代码编写遵循PEP 8标准，设计遵守python最佳实践
- 针对这个类生成测试用例

### Assistant
好的，我会按照你的要求来逐步回答：