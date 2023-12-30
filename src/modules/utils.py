import json

def custom_value_serializer(value):
    if isinstance(value, dict):
        return json.dumps(value).encode()
    elif isinstance(value, str):
        return value.encode()
    else:
        raise TypeError(f"Unsupported value type: {type(value)}")
