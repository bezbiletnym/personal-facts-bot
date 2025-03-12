import requests, bs4, yaml

def read_config() -> dict:
    config_data = {}
    try:
        with open('./config.yaml') as f:
            config_data = yaml.safe_load(f)
    except Exception as err:
        print(f"Unable to read the config file: {repr(err)}")
    return config_data

def send_tg_message(token='', chat_id=0, message='') -> bool:
    x = requests.get(
        f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}')
    return x.ok

config = read_config()
print(send_tg_message(token=config.get('BOT_TOKEN', ''), chat_id=config.get('CHAT_ID', 0), message='br'))

