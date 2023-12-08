### gpt3.5 生成

# import ast
# import astunparse
# import sys

# def extract_functions_from_patch(patch_content):
#     functions = {}
#     tree = ast.parse(patch_content)
#     for node in ast.walk(tree):
#         if isinstance(node, ast.FunctionDef):
#             functions[node.name] = astunparse.unparse(node)
#     return functions

# def replace_functions(original_content, new_functions):
#     tree = ast.parse(original_content)

#     class ReplaceFunctions(ast.NodeTransformer):
#         def visit_FunctionDef(self, node):
#             if node.name in new_functions:
#                 new_node = ast.parse(new_functions[node.name]).body[0]
#                 return new_node
#             return node

#     transformer = ReplaceFunctions()
#     transformed_tree = transformer.visit(tree)
#     return astunparse.unparse(transformed_tree)

# def generate_new_file(original_file, patch_file, output_file):
#     with open(original_file, 'r') as original:
#         original_content = original.read()

#     with open(patch_file, 'r') as patch:
#         patch_content = patch.read()

#     new_functions = extract_functions_from_patch(patch_content)
#     modified_content = replace_functions(original_content, new_functions)

#     with open(output_file, 'w') as output:
#         output.write(modified_content)

# # 替换file1.py中的函数并生成新文件
# #generate_new_file('file1.py', 'patch1.py', 'new_file.py')

# claud生成
import ast
import astor
import sys
import pathlib

def patch_file(src_file, patch_file,type):
    # 读取两个文件,解析为 AST
    with open(src_file) as f1, open(patch_file) as f2:
        ast1 = ast.parse(f1.read())
        ast2 = ast.parse(f2.read())
        
    # 在 ast2 中找到类定义        
    for node in ast2.body:
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            
            # 在 ast1 中找到同名类
            for i,cls in enumerate(ast1.body):
                if isinstance(cls, ast.ClassDef) and cls.name == class_name:
                    
                    if 'class' == type:
                        ast1.body[i] = node
                        continue
                    
                    # 找到类中的函数定义,用 ast2 中的替换
                    for method in node.body:
                        if isinstance(method, ast.FunctionDef):
                            for i, m in enumerate(cls.body):                            
                                if isinstance(m, ast.FunctionDef) and m.name == method.name:
                                    cls.body[i] = method
                                    
    # 生成新的文件
    patched_filename = f"{pathlib.Path(src_file).stem}_{pathlib.Path(patch_file).stem}.py"
    with open(patched_filename, "w") as f:
        f.write(astor.to_source(ast1))
        
# if __name__ == "__main__":
#     patch_file("file1.py", "patch1.py")

if __name__ == "__main__":
    source_code = sys.argv[1]  
    patch = sys.argv[2]
    type = sys.argv[3]
    if type not in ['func','class']:
        type = 'func'
    
    patch_file(source_code,patch,type)