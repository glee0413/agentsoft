import httpx
import asyncio
import json
from loguru import logger

class FeishuClient(object):
    """
    参考文档：https://open.feishu.cn/document/server-docs/im-v1/message/read_users
    调试路径：https://open.feishu.cn/api-explorer/cli_a519c0f9183a1013?apiName=read_users&from=op_doc&project=im&resource=message&version=v1
    """
    def __init__(self, app_id, app_secret, lark_host):
        self._app_id = app_id
        self._app_secret = app_secret
        self._lark_host = lark_host
        self._tenant_access_token = ""
        self._header = {}
        self._lark_host = 'https://open.feishu.cn'
        #await self._authorize_tenant_access_token()
        
    @property
    async def tenant_access_token(self):
        if len(self._tenant_access_token) == 0:
            await self._authorize_tenant_access_token()
        return self._tenant_access_token
    
    async def _authorize_tenant_access_token(self):
        # get tenant_access_token and set, implemented based on Feishu open api capability. doc link: https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal
        TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal"
        url = "{}{}".format(self._lark_host, TENANT_ACCESS_TOKEN_URI)
        req_body = {"app_id": self._app_id, "app_secret": self._app_secret}
        # response = requests.post(url, req_body)
        # MessageApiClient._check_error_response(response)
        # self._tenant_access_token = response.json().get("tenant_access_token")
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=req_body)
            response.raise_for_status()
            self._tenant_access_token = response.json().get("tenant_access_token")

        self._header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self._tenant_access_token,
        }
    
    async def send_message(self,receive_id_type:str,receive_id:str,
                           msg_type:str,content:str):
        url = f"{self._lark_host}/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
        req_body = {
            "receive_id": receive_id,
            "content": content,
            "msg_type": msg_type,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url=url,headers=self._header,data=req_body)
        
        logger.info(response)
        return
    
    async def reply(self,message_id:str,msg_type:str,content:str):
        url = f"{self._lark_host}/open-apis/im/v1/messages/{message_id}/reply"
        feishu_content = json.dumps({f'{msg_type}':f'{content}'})
                
        req_body = {
            "content": feishu_content,
            "msg_type": msg_type,
            "reply_in_thread": True,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url=url,headers=self._header,data=json.dumps(req_body))
        
        logger.info(response)
        
        return
    
    async def get_message(self,message_id:str, user_id_type:str):
        url = f"{self._lark_host}/open-apis/im/v1/messages/{message_id}?user_id_type={user_id_type}"
        async with httpx.AsyncClient() as client:
            response = await client.post(url=url)
        logger.info(response)
        return

async def test_feishu_api():
    client = FeishuClient("python",
                          "python",
                          "https://open.feishu.cn")
    
    print(await client.tenant_access_token)
    
    await client.reply('om_c4672ee13cda41d17c15455e3add3e62','text','hello kitti oh oh')

        
if __name__ == "__main__":
    
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_feishu_api())