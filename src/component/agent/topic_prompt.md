### System Prompt
你现在是世界知识的专家，擅长用后退的提问策略；请你深呼吸，一步步仔细思考并回答问题。

### User Message

# 软件需求规范:

## TopicBase基类需求规范
### TopicBase功能
- TopicBase可以通过protobuf格式进行转化
- TopicBase可以通过kafka进行通讯
- 类中添加如下注释
```
    TopicBase消息主要用户agent之间进行传递消息，与大模型的通讯需使用特定模型的api的数据结构
```
### TopicBase成员变量
- 关联一个格式为md5的任务id
- topic标识Id：每个topic创建时自动创建一个md5，通过此id可以关联上下文，比如在飞书里面用户可以针对客户的引用关联到不同的topic上
- topic名称
- 消息发起者
- 消息接受者
- 消息发起时间
- 消息主体内容
### TopicBase成员函数
- 填写消息

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