# System Prompt
你现在是世界知识的专家，擅长用后退的提问策略；请你深呼吸，一步步仔细思考并回答问题。
# User Message
## 软件需求规范:
""" 
### Account
#### 成员变量
名称	类型	必填	描述
api_key string 是 
api_seckey string 否 当type为“qianfan”时必填
access_count int 否 当前账户应用次数
token_count int 否 当前账户应用token数量
fail_rate float 否 当前账户的失败率
fail_count int 否 当前账户失败次数
enable bool 否 当前账户是否可用
#### 成员函数
initkey(api_key,api_seckey): 初始化账户信息
enable(bool): 使能或关闭当前账户
update(access，token_count): 如果访问成功，更新token_count

### ModelAccount说明
#### 成员变量
名称	类型	必填	描述
accounts Dict(type:string,Account) type string 是 mtype为模型类型只能是“qianfan”,"openai"，“reachai”


#### 成员函数
函数原型 说明
update_account(type,account) :更新type模型的账户信息
get_account_RR(type): 从对应模型type类型的账户,使用中使用Round Robin算法依次轮训返回一个状态为enable的账户，均衡各个账户的访问几率

"""

# 功能需求(严格按照功能需求里面的每个条目进行实现)：
- 严格完整按照webapi接口规范的描述为每个实体定义一个数据结构
- 按照规范一步一步依次实现实体类型本身定义及其schama的定义
- 第一步按照依赖关系提取接口规范中schama的定义，保证每个schema的依赖项位于本schema之前
- 请通过pydantic来进行Schema的定义
- 能够用包实现的功能用包实现，避免自己重复开发
- 正确处理异常，并在异常时发生给出清晰明确的打印提示
- 不要考虑简便性，每个功能代码都完整实现
- 代码一次生成到一个文件中
- 如果由于token限制导致代码没有完成，请再最后补充如下```continue```提醒用户操作继续生成代码

# 生成代码要求
- 请使用python实现
- 生成代码中只包含必要的包。
- 生成代码需要涵盖函数列表中列出的所有函数。
- 生成代码需要虑到执行性能、内存占用、可用性、可维护性、可扩展性。
- 生成的代码编写遵循PEP 8标准，设计遵守python最佳实践
- 针对这个类生成测试用例
- 生成类型提示，增加代码的可读性

# 生成格式要求：
其代码输出格式为markdown代码段，所有代码输出到代码块中，示例如下：
```python
import os
print('hello world')
```

# 交互式需求
如果token限制导致答案没有完全展开，需要再结束时打印如下字符串来提示用户继续完成
"""
continue
"""

# Assistant
好的，我会按照你的要求来逐步回答：