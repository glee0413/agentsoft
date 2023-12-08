### System Prompt
你现在是世界知识的专家，擅长用后退的提问策略；请你深呼吸，一步步仔细思考并回答问题。

### User Message

# 软件需求规范:

## AgentBase基类需求规范
### AgentBase功能
- AgentBase为一个虚基类
- 

## LaunchSimple基类需求规范
- 继承自LaunchBase
- 包含ConfigBase类的对象
- 读取配置文件调用ConfigBase类对象的load_json(self, filename)函数

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