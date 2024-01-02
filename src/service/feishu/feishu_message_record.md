## 直接消息
```
{
    "office_message": {
      "id": "fe05c552-2144-4203-a7ed-960f18ef3895",
      "refer_id": "",
      "meta_info": "",
      "content": "{\"text\":\"请写鸡兔同笼的问题python代码\"}",
      "sender_id": "proxy.LLM.0",
      "team_id": null,
      "receive_ids": [
        "LLM"
      ],
      "create_timestamp": "2024-01-01T08:56:25.574213"
    },
    "app_event": {
      "schema": "2.0",
      "header": {
        "event_id": "0e6fc6b9c4c9047f9d73847732e754d2",
        "event_type": "im.message.receive_v1",
        "create_time": "1704099384553",
        "token": "LUwSr560MJogoqZzoQxbIeMmEkqB44kq",
        "app_id": "cli_a5fd980539ba900e",
        "tenant_key": "1612ab78628e5740"
      },
      "event": {
        "sender": {
          "sender_id": {
            "union_id": "on_a6c9c3010bebb2de2d9080d2387b942d",
            "user_id": "bdbge882",
            "open_id": "ou_75f5f69117065340f0f7a330f4b054fa"
          },
          "sender_type": "user",
          "tenant_key": "1612ab78628e5740"
        },
        "message": {
          "message_id": "om_5404dc52a18c7e0e7666025e6ca90ab5",
          "parent_id": null,
          "root_id": null,
          "create_time": "1704099384316",
          "update_time": "1704099384316",
          "chat_id": "oc_ba1e4e5ae2341aa5656f353df8c29b84",
          "chat_type": "p2p",
          "message_type": "text",
          "content": "{\"text\":\"请写鸡兔同笼的问题python代码\"}",
          "mentions": null,
          "user_agent": null
        }
      }
    }
  }
```
## 带回复的消息
```
{
    "office_message": {
      "id": "00c5c6d6-49ce-4042-8ffd-0c2b5d66d429",
      "refer_id": "",
      "meta_info": "",
      "content": "{\"text\":\"用c语言实现\"}",
      "sender_id": "proxy.LLM.0",
      "team_id": null,
      "receive_ids": [
        "LLM"
      ],
      "create_timestamp": "2024-01-01T08:57:27.590742"
    },
    "app_event": {
      "schema": "2.0",
      "header": {
        "event_id": "1fee57174dc61c024377556465a79301",
        "event_type": "im.message.receive_v1",
        "create_time": "1704099446904",
        "token": "LUwSr560MJogoqZzoQxbIeMmEkqB44kq",
        "app_id": "cli_a5fd980539ba900e",
        "tenant_key": "1612ab78628e5740"
      },
      "event": {
        "sender": {
          "sender_id": {
            "union_id": "on_a6c9c3010bebb2de2d9080d2387b942d",
            "user_id": "bdbge882",
            "open_id": "ou_75f5f69117065340fck0f7a330f4b054fa"
          },
          "sender_type": "user",
          "tenant_key": "1612ab78628e5740"
        },
        "message": {
          "message_id": "om_80d02625d1fb85292d840b9ad0787074",
          "parent_id": "om_d43a184c87c7f064506daab36a5892db",
          "root_id": "om_d43a184c87c7f064506daab36a5892db",
          "create_time": "1704099446711",
          "update_time": "1704099446711",
          "chat_id": "oc_ba1e4e5ae2341aa5656f353df8c29b84",
          "chat_type": "p2p",
          "message_type": "text",
          "content": "{\"text\":\"用c语言实现\"}",
          "mentions": null,
          "user_agent": null
        }
      }
    }
  }
```

## 群聊信息
```
{
    "schema": "2.0",
    "header": {
        "event_id": "5e3702a84e847582be8db7fb73283c02",
        "event_type": "im.message.receive_v1",
        "create_time": "1608725989000",
        "token": "rvaYgkND1GOiu5MM0E1rncYC6PLtF7JV",
        "app_id": "cli_9f5343c580712544",
        "tenant_key": "2ca1d211f64f6438"
    },
    "event": {
        "sender": {
            "sender_id": {
                "union_id": "on_8ed6aa67826108097d9ee143816345",
                "user_id": "e33ggbyz",
                "open_id": "ou_84aad35d084aa403a838cf73ee18467"
            },
            "sender_type": "user",
            "tenant_key": "736588c9260f175e"
        },
        "message": {
            "message_id": "om_5ce6d572455d361153b7cb51da133945",
            "root_id": "om_5ce6d572455d361153b7cb5xxfsdfsdfdsf",
            "parent_id": "om_5ce6d572455d361153b7cb5xxfsdfsdfdsf",
            "create_time": "1609073151345",
            "update_time": "1687343654666",
            "chat_id": "oc_5ce6d572455d361153b7xx51da133945",
            "chat_type": "group",
            "message_type": "text",
            "content": "{\"text\":\"@_user_1 hello\"}",
            "mentions": [
                {
                    "key": "@_user_1",
                    "id": {
                        "union_id": "on_8ed6aa67826108097d9ee143816345",
                        "user_id": "e33ggbyz",
                        "open_id": "ou_84aad35d084aa403a838cf73ee18467"
                    },
                    "name": "Tom",
                    "tenant_key": "736588c9260f175e"
                }
            ],
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.53 Safari/537.36 Lark/6.7.5 LarkLocale/en_US ttnet SDK-Version/6.7.8"
        }
    }
}
```