from enum import Enum

class ErrorType(Enum):
    ET_OK = (0,'OK')
    ET_NOMATCH_OFFICE_ID = ('-1','')
    INVALID_OFFICE_ID = ('-1','非法的ID')
    def __init__(self, value, description):
        self._value_ = value
        self.description = description

    def __str__(self):
        return self.description

class ProfessionType(Enum):
    PT_CHAT = ('chat',"一般性的知识解答")
    PT_PM = ('pm','项目经理:负责项目的进度管理,git')
    PT_ARCHITECT = ('architect','架构师，负责架构任务分解，程序类图及接口设计')
    PT_CODER_PYTHON = ('python coder','负责python代码编写')
    PT_TEST_PYTHON = ('python tester','负责python测试代码的编写及测试问题提交')
    PT_OP = ('operater','负责环境构建，版本发布')
    
    def __init__(self, value, description):
        self._value_ = value
        self.description = description
    def __str__(self):
        return self.description



def test_main():
    # 使用示例
    print(ProfessionType.PT_CHAT)  # 输出：圆周率
    
if __name__ == "__main__":
    test_main()