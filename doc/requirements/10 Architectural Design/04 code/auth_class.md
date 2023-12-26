
```mermaid
---
title: 认证统计管理
---
classDiagram
    class Usage{
            +int token_limit
            +int QPS
            +List[String] llm_model 
        }

        class User{
            +String id
            +String name
        }

        class UserLimit{
            +String user_id
            +Usage usage
        }
        UserLimit "1" --> "1" User
        UserLimit "1" --> "1" Usage

```