import ast

new_function="""
def load_config_ex(self, config_file: ConfigFile):
        # 从配置文件加载配置，选择要使用的模型
        # 在这里读取配置的代码...
        print(f"Loading config: {config_file.config_key} = {config_file.config_value}")
"""

def replace_load_config_with_load_config_ex(source_code):
    # 使用ast模块解析源代码
    tree = ast.parse(source_code)
    new_node = ast.parse(new_function)
    # 定义一个替换load_config函数的访问者类
    class ReplaceLoadConfig(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            if node.name == "load_config":
                # 替换load_config函数的参数和主体
                # node.args = ast.arguments(args=[ast.arg(arg='self', annotation=None), ast.arg(arg='config_file', annotation=ast.Name(id='ConfigFile', ctx=ast.Load()))], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[])
                # node.body = [ast.Expr(value=ast.Call(func=ast.Attribute(value=ast.Name(id='print', ctx=ast.Load()), attr='format', ctx=ast.Load()), args=[ast.Str(s="Loading config: {config_file.config_key} = {config_file.config_value}")], keywords=[]))]
                node = new_node

            return self.generic_visit(node)

    # 创建访问者对象
    replace_visitor = ReplaceLoadConfig()

    # 应用访问者来修改AST
    tree = replace_visitor.visit(tree)

    # 将修改后的AST转换回源代码
    modified_code = ast.unparse(tree)
    
    return modified_code

# 读取LLMAdapter.py文件
file_path = "./LLMAdapter.py"
with open(file_path, "r") as file:
    source_code = file.read()



# 替换load_config函数为load_config_ex函数
modified_code = replace_load_config_with_load_config_ex(source_code)

# 将修改后的代码写回LLMAdapter.py文件
with open('./LLMAdapter_new.py', "w") as file:
    file.write(modified_code)

print("load_config function replaced with load_config_ex in LLMAdapter.py")
