import json
from functools import wraps
from loguru import logger
import pickle
import json
import os
from config.constant import ProfessionType


def custom_value_serializer(value):
    if isinstance(value, dict):
        return json.dumps(value).encode()
    elif isinstance(value, str):
        return value.encode()
    else:
        raise TypeError(f"Unsupported value type: {type(value)}")

def record_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        params = {'args': args, 'kwargs': kwargs}
        logger.info({func.__name__,json.dumps(params)})
        return func(*args, **kwargs)
    return wrapper


@record_args
@logger.catch
def my_function(a, b):
    return a / b

def main():
    my_function(1, 2)
    my_function(3, 0)
    
    # logger.info("Dumping recorded args to file")
    # logger.debug(logger._core.handlers[0])

    # with open('args_dump.pkl', 'wb') as file:
    #     pickle.dump(logger._core.handlers[0].sink.records, file)

    return

def test():
    profession = 'LLM'
    if not any( profession == item.value for item in ProfessionType):
            logger.error(f'unknown message profession {profession}')
    else:
        print('OK')
            
    # if not any( print(item.value) for item in ProfessionType):
    #         logger.error(f'unknown message profession {profession}')

if __name__ == "__main__":
    log_file = os.path.basename(__file__) + '.log'
    print(log_file)
    logger.add(log_file,backtrace=True, diagnose=True,rotation="500 MB",serialize=True)
    
    #main()
    test()