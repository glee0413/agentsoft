from typing import Optional, Dict, Union

from pydantic import BaseModel


class Account(BaseModel):
    api_key: Union[str, None]
    api_seckey: Union[str, None]
    access_count: Union[str, None]
    token_count: Union[str, None]
    fail_rate: Union[str, None]
    fail_count: Union[str, None]
    enable: Union[bool, None]


class ModelAccount(BaseModel):
    accounts: Dict[str, Account]

    def update_account(self, mtype: str, account: Account):
        if mtype in self.accounts:
            self.accounts[mtype] = account

    def get_account_RR(self, mtype: str) -> Optional[Account]:
        accounts_list = list(self.accounts.values())
        for _ in range(len(accounts_list)):
            account = accounts_list.pop(0)
            if account.enable:
                accounts_list.append(account)
                return account
        return None


import unittest

class TestAccountModel(unittest.TestCase):
    def test_initkey(self):
        account = Account()
        account.initkey("test_key", "test_seckey")
        self.assertEqual(account.api_key, "test_key")
        self.assertEqual(account.api_seckey, "test_seckey")

    def test_enable(self):
        account = Account()
        account.enable(False)
        self.assertFalse(account.enable)

    def test_update(self):
        account = Account()
        account.update(10, 5)
        self.assertEqual(account.access_count, 10)
        self.assertEqual(account.token_count, 5)

class TestModelAccountModel(unittest.TestCase):
    def test_update_account(self):
        model_account = ModelAccount(accounts={"qianfan": Account()})
        new_account = Account(api_key="new_key", enable=True)
        model_account.update_account("qianfan", new_account)
        self.assertEqual(model_account.accounts["qianfan"].api_key, "new_key")

    def test_get_account_RR(self):
        model_account = ModelAccount(accounts={"qianfan": Account(enable=True), "openai": Account(enable=False)})
        account = model_account.get_account_RR("qianfan")
        self.assertEqual(account.api_key, "qianfan_key")  # Assuming api_key is "qianfan_key" for testing
        self.assertTrue(account.enable)

class TestWebApiModel(unittest.TestCase):
    def test_some_webapi_function(self):
        model_account = ModelAccount(accounts={"qianfan": Account(api_key="qianfan_key", enable=True)})
        web_api = WebApi(model_account=model_account)
        result = web_api.some_webapi_function("param1_value", 42)
        self.assertEqual(result, "expected_result")  # Assuming expected_result for testing

if __name__ == '__main__':
    unittest.main()
