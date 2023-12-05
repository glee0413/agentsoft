import json
class ConfigBase:
    def __init__(self):
        self.config_dict = dict()
        self.config_dict['llm_config'] = {}
        self.config_dict['llm_config']['baidu_api'] = {}
        
        baidu_config = self.config_dict['llm_config']['baidu_api']
        baidu_config['base_url'] = ''
        baidu_config['api_id'] = 'xxxx'
        baidu_config['api_key'] = 'xxxx'
        baidu_config['api_secret_key'] = 'xxxx'
        
        self.config_dict['llm_config']['openai_api'] = {}
        openai_api_config = self.config_dict['llm_config']['openai_api']
        openai_api_config['api_key'] = 'sk-xxxx'
        openai_api_config['base_url'] = 'xxxx'
        
        # third
        self.config_dict['third_app'] = {}
        self.config_dict['third_app']['feishu'] = {}
        
        feishu_config = self.config_dict['third_app']['feishu']
        feishu_config["app_id"] = 'xxxx'
        feishu_config['app_secret'] = 'xxxx'
    
    def dump_json(self, filename):
        config_json = json.dumps(self.config_dict,indent=4)
        with open(filename, 'w') as f:
            f.write(config_json)
    def load_json(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.config_dict.update(data)
    def show_config(self):
        print(self.config_dict)
        
def main():
    config = ConfigBase()
    config.show_config()
    print('update')
    config.load_json('base_config.json')
    config.show_config()
    

if __name__ == "__main__":
    main()