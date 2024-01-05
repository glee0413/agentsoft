from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import BaseModel,Field
import os
import json

class FeishuConfigItem(BaseModel):
    app_id: str
    app_secret: str
    verification_token: str
    encrypt_key: str
    lark_host: str
    

def create_feishu_config():


    dict = {}
    dict['LLM'] = {'app_id':'cli_a5fd980539ba900e',
                                   "app_secret":'3IbSRqBcXnvxwFilvs2vIhxjZSb5zFfM',
                                   "verification_token":'LUwSr560MJogoqZzoQxbIeMmEkqB44kq',
                                   "encrypt_key":'',
                                   "lark_host":'https://open.feishu.cn'
                                   }
    
    dict['PythonExpert'] = {'app_id':'cli_a519c0462ff9500d',
                                   'app_secret':'zsjlVL1YNrxPpgg4HM24fVAEqrDaERgM',
                                   'verification_token':'2hvPxbiYvUlNWg5y3M4gPhBScH5gdIBn',
                                   'encrypt_key':'',
                                   'lark_host':'https://open.feishu.cn'}
    
    with open('feishu.json','w') as f:
        json.dump(dict,f,indent=4)

def read_feishu_config():
    with open('feishu.json','r') as f:
        data = json.load(f)
        item = {}
        for key in data.keys():
            print(key,data[key])
            item[key] = FeishuConfigItem(**data[key])
            
        print(item['LLM'])

def main():
    # create_feishu_config()
    read_feishu_config()
    return

if __name__ == "__main__":
    main()