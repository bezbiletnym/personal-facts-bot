import requests, bs4, yaml

archive_url = "https://nowiknow.com/archives/"
random_url = "http://nowiknow.com/?random"

config_path = './config.yaml'

def read_config() -> dict:
    config_data = {}
    try:
        with open(file=config_path) as f:
            config_data = yaml.safe_load(f)
    except Exception as err:
        print(f"Unable to read the config file: {repr(err)}")
    return config_data

def write_config(data: dict):
    try:
       with open(file=config_path, mode='w') as f:
           yaml.dump(data=data, stream=f)
    except Exception as err:
        print(f"Unable to write to the config file: {repr(err)}")


def get_new_article() -> [str, bool]:
    response = requests.get(url=archive_url)
    data = response.content

    soup = bs4.BeautifulSoup(markup=data, features="html.parser")
    last_article = soup.find(name='article').a['href']
    if last_article == config.get('LAST_URL'):
        print("No new article is found, getting a random one...")
        last_article = get_random_article_url()
        from_archive = False
    else:
        print(f"Last article is {last_article}")
        from_archive = True
    return last_article, from_archive


def get_random_article_url():
    response = requests.get(url=random_url)
    return response.links.get('shortlink', {}).get('url', '')


def send_tg_message(token='', chat_id=0, message='') -> bool:
    response = requests.post(url=
        f'https://api.telegram.org/bot{token}/sendMessage',
                             json={'chat_id': chat_id,
                                   'text': message,
                                   })
    return response.ok


try_counter = 0
config = read_config()
new_article, article_is_from_archive = get_new_article()

while try_counter < 5:
    try_counter += 1

    print(f"Attempt to send message #{try_counter}")
    send_result = send_tg_message(token=config.get('BOT_TOKEN', ''), chat_id=config.get('CHAT_ID', 0), message=new_article)
    print("Message is sent" if send_result else "Something is wrong")
    if send_result:
        if article_is_from_archive:
            config.update({'LAST_URL': new_article})
            write_config(config)
        break

print("Script is finished")