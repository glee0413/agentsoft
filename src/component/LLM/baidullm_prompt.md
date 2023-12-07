# System Prompt
你现在是世界知识的专家，擅长用后退的提问策略；请你深呼吸，一步步仔细思考并回答问题。
# User Message
## 软件需求规范:
""" webapi接口规范
请求地址： https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions

请求方式： POST

### Header参数
名称	值
Content-Type	application/json
### Query参数
名称	类型	必填	描述
access_token	string	是	通过API Key和Secret Key获取的access_token，参考Access Token获取
### Body参数
名称	类型	必填	描述
messages	List(message)	是	聊天上下文信息。说明：
（1）messages成员不能为空，1个成员表示单轮对话，多个成员表示多轮对话
（2）最后一个message为当前请求的信息，前面的message为历史对话信息
（3）必须为奇数个成员，成员中message的role必须依次为user或function、assistant，第一个message的role不能是function
（4）最后一个message的content长度（即此轮对话的问题）不能超过4800 个字符，且不能超过2000 tokens
（5）如果messages中content总长度大于4800 个字符或2000 tokens，系统会依次遗忘最早的历史会话，直到content的总长度不超过4800 个字符且不超过2000 tokens
functions	List(function)	否	一个可触发函数的描述列表，说明：
（1）支持的function数量无限制
（2）functions和Messages的总长度不能超过14300个字符
temperature	float	否	说明：
（1）较高的数值会使输出更加随机，而较低的数值会使其更加集中和确定
（2）默认0.8，范围 (0, 1.0]，不能为0
（3）建议该参数和top_p只设置1个
（4）建议top_p和temperature不要同时更改
top_p	float	否	说明：
（1）影响输出文本的多样性，取值越大，生成文本的多样性越强
（2）默认0.8，取值范围 [0, 1.0]
（3）建议该参数和temperature只设置1个
（4）建议top_p和temperature不要同时更改
penalty_score	float	否	通过对已生成的token增加惩罚，减少重复生成的现象。说明：
（1）值越大表示惩罚越大
（2）默认1.0，取值范围：[1.0, 2.0]
stream	bool	否	是否以流式接口的形式返回数据，默认false
system	string	否	模型人设，主要用于人设设定，例如，你是xxx公司制作的AI助手，说明：
（1）长度限制1024个字符
（2）如果使用functions参数，不支持设定人设system
stop	List(string)	否	生成停止标识，当模型生成结果以stop中某个元素结尾时，停止文本生成。说明：
（1）每个元素长度不超过20字符
（2）最多4个元素
disable_search	bool	否	是否强制关闭实时搜索功能，默认false，表示不关闭
enable_citation	bool	否	是否开启上角标返回，说明：
（1）开启后，有概率触发搜索溯源信息search_info，search_info内容见响应参数介绍
（2）默认false，不开启
user_id	string	否	表示最终用户的唯一标识符，可以监视和检测滥用行为，防止接口恶意调用

### message说明

名称	类型	必填	描述
role	string	是	当前支持以下：
user: 表示用户
assistant: 表示对话助手
function: 表示函数
content	string	是	对话内容，说明：
（1）当前message存在function_call，且role="assistant"时可以为空，其他场景不能为空
（2）最后一个message对应的content不能为blank字符，包含空格、"\n"、“\r”、“\f”等
name	string	否	message作者；当role=function时，必填，且是响应内容中function_call中的name
function_call	function_call	否	函数调用，function call场景下第一轮对话的返回，第二轮对话作为历史信息在message中传入

### function说明

名称	类型	必填	描述
name	string	是	函数名
description	string	是	函数描述
parameters	object	是	函数请求参数，说明：
（1）JSON Schema 格式，参考JSON Schema描述
（2）如果函数没有请求参数，parameters值格式如下：
{"type": "object","properties": {}}
responses	object	否	函数响应参数，JSON Schema 格式，参考JSON Schema描述
examples	List(example)	否	function调用的一些历史示例

### example说明

名称	类型	必填	描述
role	string	是	当前支持以下：
user: 表示用户
assistant: 表示对话助手
function: 表示函数
content	string	是	对话内容，说明：
（1）当前message存在function_call，且role="assistant"时可以为空，其他场景不能为空
（2）最后一个message对应的content不能为blank字符，包含空格、"\n"、“\r”、“\f”等
name	string	否	message作者；当role=function时，必填，且是响应内容中function_call中的name
function_call	function_call	否	函数调用，function call场景下第一轮对话的返回，第二轮对话作为历史信息在message中传入


### function_call说明

名称	类型	必填	描述
name	string	是	触发的function名
arguments	string	是	请求参数
thoughts	string	否	模型思考过程

## 响应说明
名称	类型	描述
id	string	本轮对话的id
object	string	回包类型
chat.completion：多轮对话返回
created	int	时间戳
sentence_id	int	表示当前子句的序号。只有在流式接口模式下会返回该字段
is_end	bool	表示当前子句是否是最后一句。只有在流式接口模式下会返回该字段
is_truncated	bool	当前生成的结果是否被截断
finish_reason	string	输出内容标识，说明：
· normal：输出内容完全由大模型生成，未触发截断、替换
· stop：输出结果命中入参stop中指定的字段后被截断
· length：达到了最大的token数，根据EB返回结果is_truncated来截断
· content_filter：输出内容被截断、兜底、替换为**等
· function_call：调用了funtion call功能
search_info	search_info	搜索数据，当请求参数enable_citation为true并且触发搜索时，会返回该字段
result	string	对话返回结果
need_clear_history	bool	表示用户输入是否存在安全，是否关闭当前会话，清理历史会话信息
true：是，表示用户输入存在安全风险，建议关闭当前会话，清理历史会话信息
false：否，表示用户输入无安全风险
ban_round	int	当need_clear_history为true时，此字段会告知第几轮对话有敏感信息，如果是当前问题，ban_round=-1
usage	usage	token统计信息
function_call	function_call	由模型生成的函数调用，包含函数名称，和调用参数

### search_info说明

名称	类型	描述
is_beset	int	是否飞线
rewrite_query	string	EDA改写后的搜索query
search_results	List(search_result)	搜索结果列表


### search_result说明

名称	类型	描述
index	int	序号
url	string	搜索结果URL
title	string	搜索结果标题
datasource_id	string	搜索来源id


### usage说明

名称	类型	描述
prompt_tokens	int	问题tokens数
completion_tokens	int	回答tokens数
total_tokens	int	tokens总数
plugins	List(plugin_usage)	plugin消耗的tokens
plugin_usage说明

名称	类型	描述
name	string	plugin名称，chatFile：chatfile插件消耗的tokens
parse_tokens	int	解析文档tokens
abstract_tokens	int	摘要文档tokens
search_tokens	int	检索文档tokens
total_tokens	int	总tokens
function_call说明

名称	类型	描述
name	string	触发的function名
thoughts	string	模型思考过程
arguments	string	请求参数

"""
# 功能需求(严格按照功能需求里面的每个条目进行实现)：
- 严格完整按照webapi接口规范的描述为每个实体定义一个数据结构
- 按照规范一步一步依次实现实体类型本身定义及其schama的定义
- 第一步按照依赖关系提取接口规范中schama的定义，保证每个schema的依赖项位于本schema之前
- 第二步在生成的schema之后依次实现webapi接口规范中定义的每个实体的数据结构类
- 实体的数据结构类中使用marshmallow包为每个实体数据结构类型添加转换为json字符串的函数及通过json转化为该类型的类的静态函数
- 实体的数据结构类中使用marshmallow包为每个实体数据结构类型添加及通过json字符串转化为该类型的类的静态函数
- 实体的数据结构类中使用marshmallow包为每个实体数据结构类型具备校验是否符合规范的函数
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


## 补充非require的元素

# System Prompt
你现在是世界知识的专家，擅长用后退的提问策略；请你深呼吸，一步步仔细思考并回答问题。
# User Message
## 软件需求规范:
``` WebMsg.py
import LLMAdapter
from marshmallow import Schema, fields, validate, ValidationError, post_dump

class BaseSchema(Schema):
    @post_dump
    def remove_skip_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items() 
            if value is not None  
        }

class HeaderSchema(BaseSchema):
    content_type = fields.Str(required=True, validate=validate.Equal("application/json"))

class FunctionCallSchema(BaseSchema):
    name = fields.Str(required=True)
    arguments = fields.Str(required=True)
    thoughts = fields.Str()

class MessageSchema(BaseSchema):
    role = fields.Str(required=True, validate=validate.OneOf(["user", "assistant", "function"]))
    content = fields.Str(required=True)
    name = fields.Str()
    function_call = fields.Nested(FunctionCallSchema)


class ExampleSchema(BaseSchema):
    role = fields.Str(required=True, validate=validate.OneOf(["user", "assistant", "function"]))
    content = fields.Str(required=True)
    name = fields.Str()
    function_call = fields.Nested(FunctionCallSchema)

class FunctionSchema(BaseSchema):
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    parameters = fields.Dict(required=True)
    responses = fields.Dict()
    examples = fields.List(fields.Nested(ExampleSchema))

class SearchResultSchema(BaseSchema):
    index = fields.Int()
    url = fields.Str()
    title = fields.Str()
    datasource_id = fields.Str()

class SearchInfoSchema(BaseSchema):
    is_beset = fields.Int()
    rewrite_query = fields.Str()
    search_results = fields.List(fields.Nested(SearchResultSchema))

class PluginUsageSchema(BaseSchema):
    name = fields.Str()
    parse_tokens = fields.Int()
    abstract_tokens = fields.Int()
    search_tokens = fields.Int()
    total_tokens = fields.Int()

class UsageSchema(BaseSchema):
    prompt_tokens = fields.Int()
    completion_tokens = fields.Int()
    total_tokens = fields.Int()
    plugins = fields.List(fields.Nested(PluginUsageSchema))

class Header:
    def __init__(self, content_type):
        self.content_type = content_type

    def to_json(self):
        schema = HeaderSchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = HeaderSchema()
        try:
            header_dict = schema.load(json_data)
        except ValidationError as e:
            print("错误信息：{}   合法数据：{}".format(e.messages, e.valid_data))
            return None
        return Header(**header_dict)


    def is_valid(self):
        schema = HeaderSchema()
        errors = schema.validate(self.__dict__)
        return not errors

class QueryParameterSchema(BaseSchema):
    access_token = fields.Str(required=True)

class QueryParameter:
    def __init__(self, access_token):
        self.access_token = access_token

    def to_json(self):
        schema = QueryParameterSchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = QueryParameterSchema()
        return schema.load(json_data)

    def is_valid(self):
        schema = QueryParameterSchema()
        errors = schema.validate(self.__dict__)
        return not errors

class BodySchema(BaseSchema):
    messages = fields.List(fields.Nested(MessageSchema), required=True)
    functions = fields.List(fields.Nested(FunctionSchema))
    temperature = fields.Float()
    top_p = fields.Float()
    penalty_score = fields.Float()
    stream = fields.Bool()
    system = fields.Str()
    stop = fields.List(fields.Str())
    disable_search = fields.Bool()
    enable_citation = fields.Bool()
    user_id = fields.Str()

class Body:
    def __init__(self, messages, functions=None, temperature=None, top_p=None, penalty_score=None,
                 stream=None, system=None, stop=None, disable_search=None, enable_citation=None, user_id=None):
        self.messages = messages
        self.functions = functions
        self.temperature = temperature
        self.top_p = top_p
        self.penalty_score = penalty_score
        self.stream = stream
        self.system = system
        self.stop = stop
        self.disable_search = disable_search
        self.enable_citation = enable_citation
        self.user_id = user_id

    def to_json(self):
        schema = BodySchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = BodySchema()
        return schema.load(json_data)

    def is_valid(self):
        schema = BodySchema()
        errors = schema.validate(self.__dict__)
        return not errors

class Message:
    def __init__(self, role, content, name=None, function_call=None):
        self.role = role
        self.content = content
        self.name = name
        self.function_call = function_call

    def to_json(self):
        schema = MessageSchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = MessageSchema()
        return schema.load(json_data)

    def is_valid(self):
        schema = MessageSchema()
        errors = schema.validate(self.__dict__)
        return not errors

class Function:
    def __init__(self, name, description, parameters, responses=None, examples=None):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.responses = responses
        self.examples = examples

    def to_json(self):
        schema = FunctionSchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = FunctionSchema()
        return schema.load(json_data)

    def is_valid(self):
        schema = FunctionSchema()
        errors = schema.validate(self.__dict__)
        return not errors

class Example:
    def __init__(self, role, content, name=None, function_call=None):
        self.role = role
        self.content = content
        self.name = name
        self.function_call = function_call

    def to_json(self):
        schema = ExampleSchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = ExampleSchema()
        return schema.load(json_data)

    def is_valid(self):
        schema = ExampleSchema()
        errors = schema.validate(self.__dict__)
        return not errors

class FunctionCall:
    def __init__(self, name, arguments, thoughts=None):
        self.name = name
        self.arguments = arguments
        self.thoughts = thoughts

    def to_json(self):
        schema = FunctionCallSchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = FunctionCallSchema()
        return schema.load(json_data)

    def is_valid(self):
        schema = FunctionCallSchema()
        errors = schema.validate(self.__dict__)
        return not errors


class ResponseSchema(BaseSchema):
    id = fields.Str()
    object = fields.Str(validate=validate.Equal("chat.completion"))
    created = fields.Int()
    sentence_id = fields.Int()
    is_end = fields.Bool()
    is_truncated = fields.Bool()
    finish_reason = fields.Str(validate=validate.OneOf(["normal", "stop", "length", "content_filter", "function_call"]))
    search_info = fields.Nested(SearchInfoSchema)
    result = fields.Str()
    need_clear_history = fields.Bool()
    ban_round = fields.Int()
    usage = fields.Nested(UsageSchema)
    function_call = fields.Nested(FunctionCallSchema)

class Response:
    def __init__(self, id, object, created, sentence_id, is_end, is_truncated, finish_reason, search_info,
                 result, need_clear_history, ban_round, usage, function_call):
        self.id = id
        self.object = object
        self.created = created
        self.sentence_id = sentence_id
        self.is_end = is_end
        self.is_truncated = is_truncated
        self.finish_reason = finish_reason
        self.search_info = search_info
        self.result = result
        self.need_clear_history = need_clear_history
        self.ban_round = ban_round
        self.usage = usage
        self.function_call = function_call

    def to_json(self):
        schema = ResponseSchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = ResponseSchema()
        return schema.load(json_data)

    def is_valid(self):
        schema = ResponseSchema()
        errors = schema.validate(self.__dict__)
        return not errors

class SearchInfo:
    def __init__(self, is_beset, rewrite_query, search_results):
        self.is_beset = is_beset
        self.rewrite_query = rewrite_query
        self.search_results = search_results

    def to_json(self):
        schema = SearchInfoSchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = SearchInfoSchema()
        return schema.load(json_data)

    def is_valid(self):
        schema = SearchInfoSchema()
        errors = schema.validate(self.__dict__)
        return not errors

class SearchResult:
    def __init__(self, index, url, title, datasource_id):
        self.index = index
        self.url = url
        self.title = title
        self.datasource_id = datasource_id

    def to_json(self):
        schema = SearchResultSchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = SearchResultSchema()
        return schema.load(json_data)

    def is_valid(self):
        schema = SearchResultSchema()
        errors = schema.validate(self.__dict__)
        return not errors

class Usage:
    def __init__(self, prompt_tokens, completion_tokens, total_tokens, plugins):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens
        self.plugins = plugins

    def to_json(self):
        schema = UsageSchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = UsageSchema()
        return schema.load(json_data)

    def is_valid(self):
        schema = UsageSchema()
        errors = schema.validate(self.__dict__)
        return not errors

class PluginUsage:
    def __init__(self, name, parse_tokens, abstract_tokens, search_tokens, total_tokens):
        self.name = name
        self.parse_tokens = parse_tokens
        self.abstract_tokens = abstract_tokens
        self.search_tokens = search_tokens
        self.total_tokens = total_tokens

    def to_json(self):
        schema = PluginUsageSchema()
        return schema.dump(self)

    @staticmethod
    def from_json(json_data):
        schema = PluginUsageSchema()
        return schema.load(json_data)

    def is_valid(self):
        schema = PluginUsageSchema()
        errors = schema.validate(self.__dict__)
        return not errors

```
# 功能需求(严格按照功能需求里面的每个条目进行实现)：
- 识别上面你提到的WebMsg.py代码中的每个继承自BaseSchema的类型
- 针对识别出来的类型中的每个变量，该变量如果没有“required=True”参数，则添加“required=False,allow_none=True”
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