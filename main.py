import requests, bs4, yaml, os
from classes.article import Article
import dotenv

def read_config() -> dict:
    config_data = {}
    try:
        with open(file=CONFIG_FILE) as f:
            config_data = yaml.safe_load(f)
            f.close()
    except Exception as err:
        print(f"Unable to read the config file: {repr(err)}")
    return config_data


def write_config(data: dict):
    try:
       with open(file=CONFIG_FILE, mode='w') as f:
           yaml.safe_dump(data=data, stream=f)
           f.close()
    except Exception as err:
        print(f"Unable to write to the config file: {repr(err)}")


def get_new_article() -> Article:
    response = requests.get(url=config.get('ARCHIVE_URL', ''))
    data = response.content

    soup = bs4.BeautifulSoup(markup=data, features="html.parser")
    last_article_url = soup.find(name='article').a['href']
    if last_article_url == config.get('LAST_URL'):
        print("No new article is found, getting a random one...")
        last_article_url = get_random_article_url()
        is_from_archive = False
    else:
        print(f"Last article is {last_article_url}")
        is_from_archive = True
    article = Article(url=last_article_url, is_from_archive=is_from_archive)
    return article


def get_random_article_url():
    response = requests.get(url=config.get('RANDOM_URL', ''))
    return response.links.get('shortlink', {}).get('url', '')


def send_tg_message(token: str, chat_id: int, article: Article) -> bool:
    tg_api_link = f"https://api.telegram.org/bot{token}/"
    message = f"<b>{article.header}</b>\n{article.url}"
    if article.pic is None:
        response = requests.post(url=f'{tg_api_link}sendMessage',
                                 json={'chat_id': chat_id,
                                        'text': message,
                                        'parse_mode': 'HTML',})
    else:
        response = requests.post(url=f'{tg_api_link}sendPhoto',
                                 json={'chat_id': chat_id,
                                        'caption': message,
                                        'parse_mode': 'HTML',
                                        'photo': article.pic,})
    print(response.content)
    return response.ok


CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "config.yaml")
dotenv.load_dotenv()
try_counter = 0
config = read_config()
new_article = get_new_article()

while try_counter < 5:
    try_counter += 1

    print(f"Attempt to send message #{try_counter}")
    send_result = send_tg_message(token=os.environ.get('BOT_TOKEN', ''), chat_id=int(os.environ.get('CHAT_ID', 0)), article=new_article)
    print("Message is sent" if send_result else "Something is wrong")
    if send_result:
        if new_article.is_from_archive:
            config.update({'LAST_URL': new_article.url})
            write_config(config)
        break

print("Script is finished")