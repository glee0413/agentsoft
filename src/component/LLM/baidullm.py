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


#######################################################################
# 测试用例
def test_entities():
    # Test Header
    header_data = {"content_type": "application/json"}
    header = Header.from_json(header_data)
    assert header.is_valid()
    assert header.to_json() == header_data

    # Test QueryParameter
    query_parameter_data = {"access_token": "your_access_token"}
    query_parameter = QueryParameter.from_json(query_parameter_data)
    print(query_parameter)
    assert query_parameter.is_valid()
    assert query_parameter.to_json() == query_parameter_data

    # Test Body
    message_data = {"role": "user", "content": "Hello, how are you?"}
    message = Message.from_json(message_data)
    body_data = {"messages": [message], "temperature": 0.8}
    body = Body.from_json(body_data)
    assert body.is_valid()
    assert body.to_json() == body_data

    # Test Function
    function_data = {"name": "example_function", "description": "An example function", "parameters": {"param": "value"}}
    function = Function.from_json(function_data)
    assert function.is_valid()
    assert function.to_json() == function_data

    # Test Example
    example_data = {"role": "user", "content": "Tell me a joke"}
    example = Example.from_json(example_data)
    assert example.is_valid()
    assert example.to_json() == example_data

    # Test FunctionCall
    function_call_data = {"name": "example_function", "arguments": "param=value"}
    function_call = FunctionCall.from_json(function_call_data)
    assert function_call.is_valid()
    assert function_call.to_json() == function_call_data

    # Test Response
    search_result_data = {"index": 1, "url": "https://example.com", "title": "Example Title", "datasource_id": "123"}
    search_result = SearchResult.from_json(search_result_data)
    search_info_data = {"is_beset": 0, "rewrite_query": "example query", "search_results": [search_result]}
    search_info = SearchInfo.from_json(search_info_data)
    response_data = {
        "id": "123456",
        "object": "chat.completion",
        "created": 1234567890,
        "sentence_id": 1,
        "is_end": True,
        "is_truncated": False,
        "finish_reason": "normal",
        "search_info": search_info,
        "result": "This is the generated result",
        "need_clear_history": False,
        "ban_round": -1,
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30, "plugins": []},
        "function_call": function_call.to_json()
    }
    response = Response.from_json(response_data)
    assert response.is_valid()
    assert response.to_json() == response_data

    # Test Usage
    plugin_usage_data = {"name": "example_plugin", "parse_tokens": 5, "abstract_tokens": 5, "search_tokens": 10, "total_tokens": 20}
    plugin_usage = PluginUsage.from_json(plugin_usage_data)
    usage_data = {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30, "plugins": [plugin_usage]}
    usage = Usage.from_json(usage_data)
    assert usage.is_valid()
    assert usage.to_json() == usage_data

    print("All test cases passed!")


#######################################################################

# @LLMAdapter.register_model("baidu-model")
# class BaiduModel:
#     # 实现百度大模型的相关功能
#     pass

if __name__ == '__main__':
    # Run the test
    test_entities()