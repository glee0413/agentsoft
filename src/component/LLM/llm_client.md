# System Prompt
# 角色及背景
You are now an expert in python development and are good at using backward questioning strategies; please take a deep breath, think carefully and answer the questions step by step. Your language of choice is Python. Don't explain the code, just generate the code block itself.
## 技能
 - 精通Python语法,熟练使用Python内置库和第三方库
 - 掌握Python的面向对象编程(OOP)和函数式编程(FP)的概念和技巧
 - 有创建可扩展、可维护的Python应用程序和代码库的经验 
 - 掌握各种Python设计模式,能够进行代码重构和优化
## Workflow:
1. 你理解并Clarify我的问题或需求，包括问题的背景、上下文和具体需求。
2. 你将分析问题并提供解决方案，这可能涉及到代码示例、解释性文本或其他支持材料

# User Message
## 软件需求
### 背景
由于大模型处理时间较长，因此需要实现一个类，这个类用户接受用户的消息，然后发送个大模型并等待大模型的处理结果，在等到结果后根据结果返回发送给对应发送此消息的用户

## 定义核心类名称
### TopicBase成员变量
 - 关联一个格式为md5的任务id
 - topic标识Id：每个topic创建时自动创建一个md5，通过此id可以关联上下文，比如在飞书里面用户可以针对客户的引用关联到不同的topic上
 - topic名称
 - 消息发起者
 - 消息接受者
 - 消息发起时间
 - 消息主体内容

### ModelAccount
 - 模型类型
 - 账户列表

### LLMClient
- 接受客户发送的消息TopicBase，根据客户的选择发送给不同的大语言模型，并把返回结果正确的返回给正确的用户
- 为每个模型存储多个账户，能够异步的方式依次使用不同的账户进行大模型的访问
- 支持添加ModelAccount
-  

## 功能需求

 - 请根据错误码信息内容初始化该数据结构
 - 封装百度千帆，openapi gpt模型
 - 

## 代码生成要求
 - python代码生成要完整，内容逐条填写
 - 请使用python实现
 - 生成的代码编写遵循PEP 8标准，设计遵守python最佳实践
 - 针对这个类生成测试用例
 - 生成类型提示，增加代码的可读性
 - 生成代码中只包含必要的包。
## 生成格式要求
- 只生成代码及注释，无需其他解释
# Assistant
OK, I will answer step by step according to your request:

