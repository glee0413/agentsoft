# 统一消息中间件
实现websocket，rabbitmq，redis，kafka，rocketmq，feishu等消息中间
## 中间件MessageTransfer
提供标准接口用于消息的发送和接收，被不同的客户端和服务器使用
提供时间信息回调

## PostOffice
配置消息中间件，屏蔽agent对于消息机制的理解
运行机制：独立运行守护进程
功能：
    独立一个消息中转站，负责接收来自各中中间件的消息
    更具消息进行路由，发送给各个消息实体

## agent
每个agent一个进程
使用消息中间件想PostOffice注册