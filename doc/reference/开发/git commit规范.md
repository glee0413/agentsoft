```
<type>(<scope>): <subject>

<body>

<footer>

<type>: 描述提交的类型，常见的类型包括：feat（新功能）、fix（修复bug）、docs（文档修改）、style（代码格式调整）、refactor（重构代码）、test（添加或修改测试代码）、chore（构建过程或工具的变动）等。
<scope>: 可选项，用于描述本次提交涉及的范围，比如模块、组件、文件等。可以根据实际情况决定是否使用。
<subject>: 简明扼要地描述本次提交的目的或内容。使用一句话进行总结，使用动词开头，使用一般现在时。比如 "修复登录页面的样式问题"、"添加用户管理功能"。
<body>: 可选项，用于详细描述本次提交的具体内容。可以包括更多的细节、原因、解决方案等。
<footer>: 可选项，用于添加与本次提交相关的链接、引用、关闭的Issue等额外信息。
```


```
feat(user-management): Add ability to delete users

- Implemented delete functionality in the user management module
- Added confirmation dialog to prompt user before deleting
- Updated UI to reflect changes after deletion

Closes #123
```